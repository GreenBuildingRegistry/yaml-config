#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2016 Earth Advantage. All rights reserved.
..codeauthor::Paul Munday <paul@paulmunday.net>

Custom Exceptions/Errors
"""


class ConfigError(Exception):
    """Indicates an error when trying to obtain a config value."""
    pass
