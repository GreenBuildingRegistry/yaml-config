#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2018 Earth Advantage. All rights reserved.
..codeauthor::Paul Munday <paul@paulmunday.net>

Tests for utils
"""

# Imports from Standard Library
import unittest

# Local Imports
from yamlconf.utils import alphasnake


class AlphasnakeTests(unittest.TestCase):
    def test_lower_case(self):
        self.assertEqual('lower', alphasnake('lower#'))
        self.assertEqual('lower_lower', alphasnake('lower# lower'))

    def test_upper_case(self):
        self.assertEqual('upper', alphasnake('UPPER#'))
        self.assertEqual('upper_upper', alphasnake('UPPER# UPPER'))

    def test_camel_case(self):
        self.assertEqual('camel_case', alphasnake('CamelCase'))
        self.assertEqual('camel_case', alphasnake('CamelCase#'))
        self.assertEqual('camel_case', alphasnake('Camel#Case'))

    def test_dromedory_case(self):
        self.assertEqual('dromedory_case', alphasnake('dromedoryCase'))
        self.assertEqual('dromedory_case', alphasnake('dromedoryCase#'))
        self.assertEqual('dromedory_case', alphasnake('dromedory#Case'))
