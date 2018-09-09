#!/usr/bin/env python
# encoding: utf-8
"""
copyright (c) 2016 Earth Advantage. All rights reserved.
..codeauthor::Paul Munday <paul@paulmunday.net>,
              Fable Turas <fable@raintechpdx.com>

Utility functions for text translations etc.
"""

# Imports from Standard Library
import collections
import os
import re
import unicodedata
from datetime import date, datetime
from importlib import import_module
from typing import (  # noqa pylint: disable=unused-import
    Any,
    Mapping,
    Optional,
    Sequence,
)

# Constants
VALID_CHARS = re.compile(r'\W+')     # alphannumerics and underscore
STRIP_CHAR_CATS = (
    'M', 'S', 'C', 'Nl', 'No', 'Pc', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'
)

STRIP_PUNC_CATS = ('Z', 'Pd')
STRIP_ALL_CATS = STRIP_CHAR_CATS + STRIP_PUNC_CATS


# Public Classes and Functions
def alphasnake(string):
    """Convert to snakecase removing non alpha numerics
    Word #word -> word_word.
    """
    if string:
        string = " ".join(
            [re.sub(r'\W+', '', word) for word in string.split()]
        )
        string = decamel_to_snake(string)
    return string


def decamel(string):
    """"Split CamelCased words.

    CamelCase -> Camel Case, dromedaryCase -> dromedary Case.
    """
    regex = re.compile(r'(\B[A-Z][a-z]*)')
    return regex.sub(r' \1', string)


def decamel_to_snake(string):
    """Convert to lower case, join camel case with underscore.
    CamelCase -> camel_case. Camel Case -> camel_case.
    """
    strings = [decamel(word) if not word.isupper() else word.lower()
               for word in string.split()]
    return "_".join([snake(dstring)for dstring in strings])


def snake(string):
    """Convert to snake case.
    Word word -> word_word
    """
    return "_".join([word.lower() for word in string.split()])
