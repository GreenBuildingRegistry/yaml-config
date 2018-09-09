#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2016 Earth Advantage. All rights reserved.
..codeauthor::Paul Munday <paul@paulmunday.net>

Tests for Config store
"""

# Imports from Standard Library
import os
import sys
import unittest
from copy import deepcopy

# Local Imports
from yamlconf import Config, ConfigError

PY3 = sys.version_info[0] == 3
if PY3:
    from unittest import mock
else:
    import mock


BASE_PATH = os.getcwd()
TEST_CONFIG_ROOT = os.path.join(BASE_PATH, 'config')
# Constants


# Helper Functions & Classes
class TESTConfig(Config):
    """Config class for TEST"""
    # pylint: disable=too-few-public-methods
    default_file = 'config.yaml'
    default_config_root = TEST_CONFIG_ROOT

    def __init__(self, config_file=None, config_dir=None, section=None):
        super(TESTConfig, self).__init__(
            config_file=config_file, config_dir=config_dir, section=section,
            env_prefix='TEST_CONFIG'
        )


# Tests
class ConfigTests(unittest.TestCase):
    """Tests for config functionality."""
    # pylint:disable=protected-access, invalid-name

    def setUp(self):
        self.env_vars = {
            'TEST_CONFIG_PATH': '/var/lib/gbr/etc',
            'TEST_CONFIG_ROOT': '/etc/gbr/conf',
            'TEST_CONFIG_PREFIX': 'TEST',
        }

    def tearDown(self):
        keys = list(self.env_vars.keys())
        keys.append('TEST_CONFIG_DIR')
        for key in keys:
            if key in os.environ:
                del os.environ[key]

    def test_get_filepath(self):
        """Test _get_filepath method."""
        conf = TESTConfig()
        with mock.patch('yamlconf.config.os.path.exists') as mock_exists:
            # no filename, not found in basepath
            mock_exists.side_effect = [False, True]
            expected = os.path.join(TEST_CONFIG_ROOT, 'config.yaml')
            result = conf._get_filepath()
            self.assertEqual(expected, result)

            # with filename, not found in basepath
            mock_exists.side_effect = [False, True]
            expected = os.path.join(TEST_CONFIG_ROOT, 'test.yaml')
            result = conf._get_filepath(filename='test.yaml')
            self.assertEqual(expected, result)

            # no filename, found in basepath
            mock_exists.side_effect = [True, False]
            expected = os.path.join(conf.basepath, 'config.yaml')
            result = conf._get_filepath()
            self.assertEqual(expected, result)

            # with filename, found in basepath
            mock_exists.side_effect = [True, False]
            expected = os.path.join(conf.basepath, 'test.yaml')
            result = conf._get_filepath(filename='test.yaml')
            self.assertEqual(expected, result)

    def test_get_filepath_with_config_root(self):
        """Test _get_filepath method with TEST_CONFIG_ROOT env var set."""
        gbr_config_root = '/var/lib/gbr/'
        os.environ['TEST_CONFIG_ROOT'] = gbr_config_root
        conf = TESTConfig()
        with mock.patch('yamlconf.config.os.path.exists') as mock_exists:
            # TEST_CONFIG_ROOT env var set, no filename, not found in basepath
            mock_exists.side_effect = [False, True]
            expected = os.path.join(gbr_config_root, 'config.yaml')
            result = conf._get_filepath()
            self.assertEqual(expected, result)

            # TEST_CONFIG_ROOT env var set, with filename, not found in
            # basepath
            mock_exists.side_effect = [False, True]
            expected = os.path.join(gbr_config_root, 'test.yaml')
            result = conf._get_filepath(filename='test.yaml')
            self.assertEqual(expected, result)

            # TEST_CONFIG_ROOT env var set, no filename, found in basepath
            mock_exists.side_effect = [True, False]
            expected = os.path.join(conf.basepath, 'config.yaml')
            result = conf._get_filepath()
            self.assertEqual(expected, result)

            # TEST_CONFIG_ROOT env var set, with filename, found in basepath
            mock_exists.side_effect = [True, False]
            expected = os.path.join(conf.basepath, 'test.yaml')
            result = conf._get_filepath(filename='test.yaml')
            self.assertEqual(expected, result)

    def test_get_filepath_with_config_path(self):
        """Test _get_filepath method with TEST_CONFIG_PATH env var set."""
        gbr_config_path = '/var/lib/gbr/'
        os.environ['TEST_CONFIG_PATH'] = gbr_config_path
        conf = TESTConfig()
        with mock.patch('yamlconf.config.os.path.exists') as mock_exists:
            # TEST_CONFIG_PATH env var set, no filename, not found in basepath
            mock_exists.side_effect = [False, True]
            expected = os.path.join(TEST_CONFIG_ROOT, 'config.yaml')
            result = conf._get_filepath()
            self.assertEqual(expected, result)

            # TEST_CONFIG_PATH env var set, with filename, not found in
            # basepath
            mock_exists.side_effect = [False, True]
            expected = os.path.join(TEST_CONFIG_ROOT, 'test.yaml')
            result = conf._get_filepath(filename='test.yaml')
            self.assertEqual(expected, result)

            # TEST_CONFIG_PATH env var set, no filename, found in basepath
            mock_exists.side_effect = [True, False]
            expected = os.path.join(gbr_config_path, 'config.yaml')
            result = conf._get_filepath()
            self.assertEqual(expected, result)

            # TEST_CONFIG_PATH env var set, with filename, found in basepath
            mock_exists.side_effect = [True, False]
            expected = os.path.join(gbr_config_path, 'test.yaml')
            result = conf._get_filepath(filename='test.yaml')
            self.assertEqual(expected, result)

    def test_get_filepath_with_config_dir(self):
        """Test _get_filepath method with config_dir set."""
        conf = TESTConfig()
        config_dir = 'test'
        with mock.patch('yamlconf.config.os.path.exists') as mock_exists:
            # no filename, not found in basepath
            mock_exists.side_effect = [False, True]
            expected = os.path.join(
                TEST_CONFIG_ROOT, config_dir, 'config.yaml')
            result = conf._get_filepath(config_dir=config_dir)
            self.assertEqual(expected, result)

            # with filename, not found in basepath
            mock_exists.side_effect = [False, True]
            expected = os.path.join(TEST_CONFIG_ROOT, config_dir, 'test.yaml')
            result = conf._get_filepath(
                filename='test.yaml', config_dir=config_dir
            )
            self.assertEqual(expected, result)

            # no filename, found in basepath
            mock_exists.side_effect = [True, False]
            expected = os.path.join(conf.basepath, config_dir, 'config.yaml')
            result = conf._get_filepath(config_dir=config_dir)
            self.assertEqual(expected, result)

            # with filename, found in basepath
            mock_exists.side_effect = [True, False]
            expected = os.path.join(conf.basepath, config_dir, 'test.yaml')
            result = conf._get_filepath(
                filename='test.yaml', config_dir=config_dir
            )
            self.assertEqual(expected, result)

    @mock.patch('yamlconf.config.os.path.exists')
    @mock.patch('yamlconf.config.os.path.dirname')
    def test_get_filepath_with_gbr_config(self, mock_dirname, mock_exists):
        """Test _get_filepath method with TEST_CONFIG env var"""
        mock_dirname.side_effect = ['foo/bar/baz', 'foo/bar/', 'foo', '/etc/']
        mock_exists.side_effect = [True, False, False]
        gbr_config = '/etc/gbr.yaml'
        os.environ['TEST_CONFIG'] = gbr_config
        with mock.patch(
            'yamlconf.config.open', mock.mock_open(read_data='{}'),
            create=True
        ):
            conf = TESTConfig()
            expected = gbr_config
            self.assertEqual(expected, conf.config_file)

    def test_init_env_vars(self):
        """Test setting attributes via environment variables."""
        for key, val in self.env_vars.items():
            os.environ[key] = val
        conf = TESTConfig()
        self.assertEqual(self.env_vars['TEST_CONFIG_PATH'], conf.basepath)
        self.assertEqual(self.env_vars['TEST_CONFIG_ROOT'], conf.config_root)
        self.assertEqual(self.env_vars['TEST_CONFIG_PREFIX'], conf.prefix)

    @mock.patch('yamlconf.config.yaml.load')
    def test_init_config_file(self, mock_load):
        """Test setting attributes via config file."""
        mock_load.return_value = {'config_prefix': 'gbr_config_prefix'}
        with mock.patch(
            'yamlconf.config.open', mock.mock_open(read_data='{}'),
            create=True
        ):
            config_path = self.env_vars['TEST_CONFIG_PATH']
            config_root = self.env_vars['TEST_CONFIG_ROOT']
            for key, val in self.env_vars.items():
                os.environ[key] = val
            os.environ['TEST_CONFIG_DIR'] = 'config'
            conf = TESTConfig()
        self.assertEqual(config_path, conf.basepath)
        self.assertEqual(config_root, conf.config_root)
        # self.assertEqual(TEST_CONFIG_ROOT, conf.basepath)
        # self.assertEqual(TEST_CONFIG_ROOT, conf.config_root)
        self.assertEqual(None, conf.config_file)
        self.assertEqual('gbr_config_prefix', conf.prefix)

    @mock.patch('yamlconf.config.yaml.load')
    @mock.patch('yamlconf.config.os.path.exists')
    @mock.patch('yamlconf.config.os.path.dirname')
    def test_init_prefix(self, mock_dirname, mock_exists, mock_load):
        """Test setting attributes via config file."""
        mock_dirname.side_effect = ['foo/bar/baz', 'foo/bar/', 'foo', '']
        mock_exists.side_effect = [False, False, True, True]
        mock_load.side_effect = [{}, {'config_prefix': 'TEST'}]
        with mock.patch(
            'yamlconf.config.open', mock.mock_open(read_data='{}'),
            create=True
        ):
            for key, val in self.env_vars.items():
                os.environ[key] = val
            os.environ['TEST_CONFIG_PREFIX'] = 'TEST'
            conf = TESTConfig()
        self.assertEqual('TEST', conf.prefix)

    def test_get_env_var(self):
        """Test get from environment var"""
        expected = 'test'
        os.environ['TEST_CONFIG_PREFIX'] = 'TEST'
        os.environ['TEST_TEST_VALUE'] = expected
        conf = TESTConfig()
        result = conf.get('value', section='test')
        self.assertEqual(expected, result)

    def test_get_env_var_underscore(self):
        """Test get from environment var works with underscore in name"""
        expected = 'under_score'
        os.environ['TEST_CONFIG_PREFIX'] = 'TEST'
        os.environ['TEST_TEST_TEST_VALUE'] = expected
        conf = TESTConfig()
        result = conf.get('test_value', section='test')
        self.assertEqual(expected, result)

    def test_get_env_default(self):
        """Test get from default"""
        conf = TESTConfig()
        result = conf.get('value2', section='test', default='default')
        self.assertEqual('default', result)

    def test_get_exception(self):
        """Test get raises exception if not found"""
        os.environ['TEST_CONFIG_PREFIX'] = 'TEST'
        conf = TESTConfig()
        conf.config_file = None     # in case a local file exists
        with self.assertRaises(ConfigError) as conm:
            conf.get('foo !3', section='test')
        exception = conm.exception
        expected = "Could not find 'foo !3' in section 'test'. "
        expected += "Checked environment variable: TEST_TEST_FOO_3"
        self.assertEqual(expected, str(exception))

        with self.assertRaises(ConfigError) as conm:
            conf.get('FOO !3', section='test')
        exception = conm.exception
        expected = "Could not find 'FOO !3' in section 'test'. "
        expected += "Checked environment variable: TEST_TEST_FOO_3"
        self.assertEqual(expected, str(exception))

    @mock.patch('yamlconf.config.yaml.load')
    @mock.patch('yamlconf.config.os.path.exists')
    @mock.patch('yamlconf.config.os.path.dirname')
    def test_get_config(self, mock_dirname, mock_exists, mock_load):
        """Test get via config file."""
        mock_dirname.side_effect = ['foo/bar/baz', 'foo/bar/', 'foo', '']
        mock_exists.side_effect = [False, False, True]
        mock_load.side_effect = [
            {'test': {'test2': 'foo'}, 'config_prefix': 'TEST'}
        ]
        with mock.patch(
            'yamlconf.config.open', mock.mock_open(read_data='{}'),
            create=True
        ):
            conf = TESTConfig()
        result = conf.get('test2', section='test', default='default')
        self.assertEqual('foo', result)

    @mock.patch('yamlconf.config.yaml.load')
    @mock.patch('yamlconf.config.os.path.exists')
    @mock.patch('yamlconf.config.os.path.dirname')
    def test_copy(self, mock_dirname, mock_exists, mock_load):
        """Test copy raises error."""
        mock_dirname.side_effect = ['foo/bar/baz', 'foo/bar/', 'foo', '']
        mock_exists.side_effect = [False, False, True]
        mock_load.side_effect = [
            {'test': {'test2': 'foo'}, 'config_prefix': 'TEST'}
        ]
        with mock.patch(
            'yamlconf.config.open', mock.mock_open(read_data='{}'),
            create=True
        ):
            conf = TESTConfig()
        with self.assertRaises(NotImplementedError) as conm:
            conf.copy()
            msg = str(conm.exception)
            self.assertEqual('Shallow copying is forbidden.', msg)

    @mock.patch('yamlconf.config.yaml.load')
    @mock.patch('yamlconf.config.os.path.exists')
    @mock.patch('yamlconf.config.os.path.dirname')
    def test_deepcopy(self, mock_dirname, mock_exists, mock_load):
        """Test deepcopy."""
        mock_dirname.side_effect = ['foo/bar/baz', 'foo/bar/', 'foo', '']
        mock_exists.side_effect = [False, False, True]
        mock_load.side_effect = [
            {'test': {'test2': 'foo'}, 'config_prefix': 'TEST'}
        ]
        with mock.patch(
            'yamlconf.config.open', mock.mock_open(read_data='{}'),
            create=True
        ):
            conf = TESTConfig()
            new = deepcopy(conf)
            self.assertEqual(new, conf.config)
            new['foo'] = 'bar'
            self.assertNotEqual(new, conf.config)

    @mock.patch('yamlconf.config.yaml.load')
    @mock.patch('yamlconf.config.os.path.exists')
    @mock.patch('yamlconf.config.os.path.dirname')
    def test_items(self, mock_dirname, mock_exists, mock_load):
        """Test items."""
        mock_dirname.side_effect = ['foo/bar/baz', 'foo/bar/', 'foo', '']
        mock_exists.side_effect = [False, False, True]
        mock_load.side_effect = [
            {'test': {'test2': 'foo'}, 'config_prefix': 'TEST'}
        ]
        with mock.patch(
            'yamlconf.config.open', mock.mock_open(read_data='{}'),
            create=True
        ):
            conf = TESTConfig(section='test')
            self.assertEqual(conf.items(), conf.config['test'].items())

    @mock.patch('yamlconf.config.yaml.load')
    @mock.patch('yamlconf.config.os.path.exists')
    @mock.patch('yamlconf.config.os.path.dirname')
    def test_keys(self, mock_dirname, mock_exists, mock_load):
        """Test keys."""
        mock_dirname.side_effect = ['foo/bar/baz', 'foo/bar/', 'foo', '']
        mock_exists.side_effect = [False, False, True]
        mock_load.side_effect = [
            {'test': {'test2': 'foo'}, 'config_prefix': 'TEST'}
        ]
        with mock.patch(
            'yamlconf.config.open', mock.mock_open(read_data='{}'),
            create=True
        ):
            conf = TESTConfig(section='test')
            self.assertEqual(conf.keys(), conf.config['test'].keys())

    @mock.patch('yamlconf.config.yaml.load')
    @mock.patch('yamlconf.config.os.path.exists')
    @mock.patch('yamlconf.config.os.path.dirname')
    def test_values(self, mock_dirname, mock_exists, mock_load):
        """Test values."""
        mock_dirname.side_effect = ['foo/bar/baz', 'foo/bar/', 'foo', '']
        mock_exists.side_effect = [False, False, True]
        mock_load.side_effect = [
            {'test': {'test2': 'foo'}, 'config_prefix': 'TEST'}
        ]
        with mock.patch(
            'yamlconf.config.open', mock.mock_open(read_data='{}'),
            create=True
        ):
            conf = TESTConfig(section='test')
            self.assertEqual(
                list(conf.values()), list(conf.config['test'].values())
            )
