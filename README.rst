YAML Config
===========

A Python client for reading yaml based config files

Documentation
-------------
YAML Config provides a Config Class for retrieving configuration variables from YAML based config files.

Recommended usage is to subclass this class to define default_file and/or default_config_root as necessary, or to override __init__ with relevant defaults.


.. code-block:: python

        class GBRConfig(Config):
            default_file = 'config.yaml'
            default_config_root = os.path.join(BASE_PATH, 'config')

            def __init__(self, config_file=None, config_dir=None, section=None):
                super(GBRConfig, self).__init__(
                    config_file=config_file, config_dir=config_dir,
                    section=section, env_prefix='GBR_CONFIG'
                )


example usage:


.. code-block:: python

        CONFIG = GBRConfig()
        TIMEZONE = CONFIG.get('timezone', default='utc')

Installation
------------


``pip install yaml-config``

You may setup environmental variables to the path and folder containing config files:
    <your_env_prefix>_DIR

    <your_env_prefix>_ROOT


``export GBR_CONFIG_ROOT=/path/to/your/config``


Contributing
------------

License
-------
yaml-config is released under the terms of the MIT license. Full details in LICENSE file.

Changelog
---------
yaml-config was developed for use in the greenbuildingregistry project.
For a full changelog see `CHANGELOG.rst <https://github.com/GreenBuildingRegistry/yaml-config/blob/master/CHANGELOG.rst>`_.