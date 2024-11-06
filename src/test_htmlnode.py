import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html2(self):
        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        self.assertNotEqual(node.props_to_html(), 'href="https://www.google.com"target="_blank"')

    def test_props_to_html3(self):
        node = HTMLNode()
        self.assertRaises(Exception, node.props_to_html)
