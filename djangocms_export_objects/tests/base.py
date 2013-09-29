#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestsBase(unittest.TestCase):

    def create_fixtures(self):
        """
        Tree from fixture:

            page1
                page2
                    page3
            page4
                page5
        """
        from cms.api import create_page
        from cms.models import Page
        defaults = {
            'template': 'index.html',
            'language': 'en',
        }
        p1 = create_page('page1', published=True, in_navigation=True, **defaults)
        p4 = create_page('page4', published=True, in_navigation=True, **defaults)
        p2 = create_page('page2', published=True, in_navigation=True, reverse_id="export", parent=p1, **defaults)
        p3 = create_page('page3', published=True, in_navigation=True, parent=p2, **defaults)
        p5 = create_page('page5', published=True, in_navigation=True, parent=p4, **defaults)
