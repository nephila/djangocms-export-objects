# -*- coding: utf-8 -*-
from __future__ import with_statement
import os
import socket

from sphinx.application import Sphinx
from six import StringIO

from .base import unittest
from .tmpdir import temp_dir

ROOT_DIR = os.path.dirname(__file__)
DOCS_DIR = os.path.abspath(os.path.join(ROOT_DIR, u'..', u'..', u'docs'))


def has_no_internet():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('4.4.4.2', 80))
        s.send(b"hello")
    except socket.error: # no internet
        return True
    return False


class DocsTestCase(unittest.TestCase):
    """
    Test docs building correctly for HTML
    """
    @unittest.skipIf(has_no_internet(), "No internet")
    def test_html(self):
        nullout = StringIO()
        with temp_dir() as OUT_DIR:
            app = Sphinx(
                DOCS_DIR,
                DOCS_DIR,
                OUT_DIR,
                OUT_DIR,
                "html",
                warningiserror=False,
                status=nullout,
            )
            try:
                app.build()
            except:
                print(nullout.getvalue())
                raise
