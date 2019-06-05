#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2016 Earth Advantage. All rights reserved.
..codeauthor::Paul Munday <paul@paulmunday.net>

Config class
"""
# pylint:disable=abstract-method

# Imports from Standard Library
import os
from copy import deepcopy

# Imports from Third Party Modules
import yaml

# Local Imports
from yamlconf.exceptions import ConfigError
from yamlconf.utils import alphasnake

BASE_PATH = os.getcwd()


def _suffix(name, suffix=None):
    """Append suffix (default _)."""
    suffix = suffix if suffix else '_'
    return "{}{}".format(name, suffix)


class Config(object):
    """Class for retrieving configuration variables.

    N.B. Recommended usage is to subclass this class to define default_file
    and/or default_config_root as necessary, or to override __init__ with
    relevant defaults.
    eg:
    class GBRConfig(Config):
        default_file = 'config.yaml'
        default_config_root = os.path.join(BASE_PATH, 'config')

        def __init__(self, config_file=None, config_dir=None, section=None):
            super(GBRConfig, self).__init__(
                config_file=config_file, config_dir=config_dir,
                section=section, env_prefix='GBR_CONFIG'
            )
    """
    # pylint: disable=too-few-public-methods, too-many-instance-attributes
    default_file = 'config.yaml'
    default_config_root = os.path.join(BASE_PATH, 'config')

    def __init__(self, config_file=None, config_dir=None, section=None,
                 env_prefix=None, loader=yaml.SafeLoader):
        if not env_prefix:
            raise ConfigError('env_prefix can not be null.')
        self.env_prefix = env_prefix
        self.config = {}
        self.prefix = None
        self.config_path = self.env_prefix + '_PATH'
        self.config_prefix = self.env_prefix + '_PREFIX'
        self.config_root_path = self.env_prefix + '_ROOT'
        self.basepath = os.getenv(
            self.config_path, default=self.default_config_root
        )
        self.config_root = os.getenv(
            self.config_root_path, default=self.default_config_root
        )
        self.section = section
        self.config_file = self._get_filepath(
            filename=config_file, config_dir=config_dir
        )
        self.loader = loader
        self.load()

    def load(self):
        """(Re)Load config file."""
        try:
            with open(self.config_file) as configfile:
                self.config = yaml.load(configfile, Loader=self.loader)
        except TypeError:
            # no config file (use environment variables)
            pass
        if self.config:
            self.prefix = self.config.get('config_prefix', None)
        if not self.prefix:
            if os.getenv(self.config_prefix):
                self.prefix = os.getenv(self.config_prefix)
            else:
                for path in [
                    os.path.join(self.basepath, self.default_file),
                    os.path.join(self.config_root, self.default_file)
                ]:
                    if os.path.exists(path):
                        with open(path) as conf:
                            config = yaml.load(conf, Loader=self.loader)
                            prefix = config.get(
                                self.config_prefix.lower(), None
                            )
                            if prefix:
                                self.prefix = prefix
                                break

    def get(self, var, section=None, **kwargs):
        """Retrieve a config var.
        Return environment variable if it exists
        (ie [self.prefix + _] + [section + _] + var)
        otherwise var from config file.

        If both are null and no default is set a ConfigError will be raised,
        otherwise default will be returned.

        :param var: key to look up
        :param default: default value, must be supplied as keyword
        """
        # default is not a specified keyword argument so we can distinguish
        # between a default set to None and no default sets
        if not section and self.section:
            section = self.section
        default = kwargs.get('default', None)
        env_var = "{}{}{}".format(
            _suffix(self.prefix) if self.prefix else '',
            _suffix(alphasnake(section)) if section else '',
            alphasnake(str(var))
        ).upper()
        config = self.config.get(section, {}) if section else self.config
        result = config.get(var, default)
        result = os.getenv(env_var, default=result)
        # no default keyword supplied (and no result)
        #  use is None to allow empty lists etc
        if result is None and 'default' not in kwargs:
            msg = "Could not find '{}'".format(var)
            if section:
                msg = "{} in section '{}'.".format(
                    msg, section
                )
            msg = "{} Checked environment variable: {}".format(msg, env_var)
            if self.config_file:
                msg = "{} and file: {}".format(msg, self.config_file)
            raise ConfigError(msg)
        return result

    def keys(self, section=None):
        """Provide dict like keys method"""
        if not section and self.section:
            section = self.section
        config = self.config.get(section, {}) if section else self.config
        return config.keys()

    def items(self, section=None):
        """Provide dict like items method"""
        if not section and self.section:
            section = self.section
        config = self.config.get(section, {}) if section else self.config
        return config.items()

    def values(self, section=None):
        """Provide dict like values method"""
        if not section and self.section:
            section = self.section
        config = self.config.get(section, {}) if section else self.config
        return config.values()

    def __copy__(self):
        raise NotImplementedError('Shallow copying is forbidden')

    def copy(self):
        """Raise error"""
        self.__copy__()

    def __deepcopy__(self, memo):
        if self.section:
            config = self.config.get(self.section, {})
        else:
            config = self.config
        return deepcopy(config, memo)

    def _get_filepath(self, filename=None, config_dir=None):
        """
        Get config file.

            :param filename: name of config file (not path)
            :param config_dir: dir name prepended to file name.

        Note: we use e.g. GBR_CONFIG_DIR here, this is the default
        value in GBR but it is actually self.env_prefix + '_DIR' etc.

        If config_dir is not supplied it will be set to the value of the
        environment variable GBR_CONFIG_DIR or None.

        If filename is not supplied and the environment variable GBR_CONFIG
        is set and contains a path, its value will be tested to see if a file
        exists, if so that is returned as the config file otherwise filename
        will be set to GBR_CONFIG, if it exists, otherwise 'config.yaml'.

        If a filename is supplied or GBR_CONFIG is not an existing file:

            If the environment variable GBR_CONFIG_PATH exists the path
            GBR_CONFIG_PATH/config_dir/filename is checked.

            If it doesn't exist config/CONFIG_DIR/filename  is checked
                (relative to the root of the (GBR) repo)
            finally GBR_CONFIG_DEFAULT/CONFIG_DIR/filename is tried

        If no file is found None will be returned.
        """
        # pylint: disable=no-self-use
        config_file = None
        config_dir_env_var = self.env_prefix + '_DIR'
        if not filename:
            # Check env vars for config
            filename = os.getenv(self.env_prefix, default=self.default_file)
            # contains path so try directly
            if os.path.dirname(filename) and os.path.exists(filename):
                config_file = filename
        if not config_file:
            # Cannot contain path
            filename = os.path.basename(filename)
            if not config_dir:
                config_dir = os.getenv(config_dir_env_var, default='')
            for path in [self.basepath, self.config_root]:
                filepath = os.path.join(path, config_dir, filename)
                if os.path.exists(filepath):
                    config_file = filepath
                    break
        return config_file
