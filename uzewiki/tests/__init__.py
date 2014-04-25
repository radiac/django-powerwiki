"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import codecs
import os

from django.test import TestCase

from uzewiki.management.commands import convert_wiki

class DokuwikiTest(TestCase):
    def test_dokuwiki_convert(self):
        # Set up converter
        test_dir, test = os.path.split(__file__)
        path = os.path.join(test_dir, 'convert_wiki', 'dokuwiki')
        converter = convert_wiki.DokuwikiConverter(path)
        
        # Check that source converts correctly
        content_doku = self.read_file(path, 'pages', 'start.txt')
        content_wiki = self.read_file(path, 'converted.pxt')
        self.assertEqual(
            content_wiki,
            converter.convert_content(content_doku)
        )

    def read_file(self, *filepath):
        file = codecs.open(os.path.join(*filepath), 'r', 'utf-8')
        return file.read()
    maxDiff = 10000