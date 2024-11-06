import unittest

from main import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import LeafNode


class TestMain(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode("bold text", TextType.BOLD)
        html_node = LeafNode("b", "bold text")
        self.assertEqual(text_node_to_html_node(text_node), html_node)

    def test_text_node_to_html_node2(self):
        text_node = TextNode("Normal text", TextType.NORMAL)
        html_node = LeafNode(None, "Normal text")
        self.assertEqual(text_node_to_html_node(text_node), html_node)

    def test_text_node_to_html_node3(self):
        text_node = TextNode("link to url", TextType.LINK, url="https://google.com")
        html_node = LeafNode("a", "link to url", props={"href": "https://google.com",})
        self.assertEqual(text_node_to_html_node(text_node), html_node)

    def test_text_node_to_html_node4(self):
        text_node = TextNode("image description", TextType.IMAGE, url="https://example.com/logo.svg")
        html_node = LeafNode("img", None, props={"src": "https://example.com/logo.svg", "alt": "image description",})
        self.assertEqual(text_node_to_html_node(text_node), html_node)
    
    def test_text_node_to_html_node5(self):
        text_node = TextNode("text", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)
