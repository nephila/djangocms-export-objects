#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from six import StringIO



class TestsBase(unittest.TestCase):
    pass