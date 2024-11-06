import unittest

from htmlnode import HTMLNode, LeafNode


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
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "a test value")
        self.assertEqual(node.to_html(), "<p>a test value</p>")

    def test_to_html2(self):
        props = {
            "href": "https://www.google.com",
        }
        node = LeafNode("a", "a beautiful link", props=props)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">a beautiful link</a>')

    def test_to_html3(self):
        props = {
            "id": "special_link",
            "href": "https://www.google.com",
        }
        node = LeafNode("a", "a beautiful link", props=props)
        self.assertEqual(node.to_html(), '<a id="special_link" href="https://www.google.com">a beautiful link</a>')   

    def test_to_html4(self):
        node = LeafNode(None, "text")
        self.assertEqual(node.to_html(), "text")

    def test_to_html5(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html6(self):
        node = LeafNode(None, "")
        self.assertRaises(ValueError, node.to_html)
    