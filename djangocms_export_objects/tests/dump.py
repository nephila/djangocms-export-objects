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

    def test_partial_dump(self):
        jdata = BytesIO()
        call_command("cms_dump_objects", "cms.Page.objects.filter(reverse_id='export')", stdout=jdata, indent=3)
        data = json.loads(jdata.getvalue())

        page_items = [item for item in data if item['model'] == 'cms.page']
        # 2 pages (page 1 and page 2)
        self.assertEqual(len(page_items), 4)

    def test_partial_dump_skip(self):
        jdata = BytesIO()
        call_command("cms_dump_objects", "cms.Page.objects.filter(reverse_id='export')", stdout=jdata, indent=3, skip_ancestors=True)
        data = json.loads(jdata.getvalue())

        page_items = [item for item in data if item['model'] == 'cms.page']
        page2 = [item for item in data if item['model'] == 'cms.title' and item['fields'].get('slug') == u'page2']
        # 1 page (page 2)
        self.assertEqual(len(page_items), 2)
        self.assertTrue(page2)

    def test_recursive_dump(self):
        jdata = BytesIO()
        call_command("cms_dump_objects", "cms.Page.objects.filter(reverse_id='export')", stdout=jdata, indent=3, skip_ancestors=True, recursive=True)
        data = json.loads(jdata.getvalue())

        page_items = [item for item in data if item['model'] == 'cms.page']
        page3 = [item for item in data if item['model'] == 'cms.title' and item['fields'].get('slug') == u'page3']

        # 1 page (page 2)
        self.assertEqual(len(page_items), 4)
        self.assertTrue(page3)

    def test_plugin_dump(self):
        from cms.models import Page
        from cms.api import add_plugin

        basepage = Page.objects.filter(reverse_id='export', published=True)[0].get_public_object()
        ph = basepage.placeholders.get(slot="ph1")

        # add random plugins
        text = add_plugin(ph, "TextPlugin", "en", body="Hello World")
        link = add_plugin(ph, "LinkPlugin", "en", target=text,
                          name="A Link", url="https://www.whatever.org")

        jdata = BytesIO()
        call_command("cms_dump_objects", "cms.Page.objects.filter(reverse_id='export')", stdout=jdata, indent=3)
        data = json.loads(jdata.getvalue())

        page_items = [item for item in data if item['model'] == 'cms.page']
        # 2 pages (page 1 and page 2)
        self.assertEqual(len(page_items), 4)

        plugin = [item for item in data if item['model'] == 'cms.cmsplugin' and item['fields'].get('plugin_type') == 'LinkPlugin']
        # 1 link plugin
        self.assertEqual(len(plugin), 1)

        plugin = [item for item in data if item['model'] == 'link.link']
        # 1 link model pobject
        self.assertEqual(plugin[0]['fields']['url'], "https://www.whatever.org")

    def tearDown(self):
        from cms.models import Page
        Page.objects.all().delete()
