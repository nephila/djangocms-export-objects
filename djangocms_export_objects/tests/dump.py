#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from io import BytesIO

from django.core.management import call_command

from .base import TestsBase


class TestDjangocmsExportObjects(TestsBase):

    def setUp(self):
        self.create_fixtures()

    def test_simple_dump(self):
        jdata = BytesIO()
        call_command("cms_dump_objects", "cms.Page.objects.all()", stdout=jdata, indent=3)
        data = json.loads(jdata.getvalue())

        page_items = [item for item in data if item['model'] == 'cms.page']
        # 5 pages, 10 page objects
        self.assertEqual(len(page_items), 10)

        title_items = [item for item in data if item['model'] == 'cms.title']
        # 5 pages, 10 titles
        self.assertEqual(len(title_items), 10)


    def tearDown(self):
        pass
