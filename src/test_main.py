import unittest

from main import text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType
from htmlnode import LeafNode


class TestMain(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode("bold text", TextType.BOLD)
        html_node = LeafNode("b", "bold text")
        self.assertEqual(text_node_to_html_node(text_node), html_node)

    def test_text_node_to_html_node2(self):
        text_node = TextNode("Normal text", TextType.TEXT)
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

    def test_split_nodes_delimiter(self):
        input_nodes = [
            TextNode("example text", TextType.TEXT),
        ]
        output_nodes = [
            TextNode("example text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(input_nodes, "**", TextType.BOLD), output_nodes)

    def test_split_nodes_delimiter2(self):
        input_nodes = [
            TextNode("example text with a **bold** word.", TextType.TEXT),
        ]
        output_nodes = [
            TextNode("example text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(input_nodes, "**", TextType.BOLD), output_nodes)

    def test_split_nodes_delimiter3(self):
        input_nodes = [
            TextNode("example text with a **bold** word.", TextType.TEXT),
            TextNode("another example text with a `code block` word.", TextType.TEXT),
        ]
        output_nodes = [
            TextNode("example text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
            TextNode("another example text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word.", TextType.TEXT),
        ]
        delimited_by_bold = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        delimited_by_code = split_nodes_delimiter(delimited_by_bold, "`", TextType.CODE)
        self.assertEqual(delimited_by_code, output_nodes)
    
    def test_split_nodes_delimiter4(self):
        input_nodes = [
            TextNode("example text with **missing closing delimiter", TextType.TEXT),
        ]
        with self.assertRaises(Exception):
            split_nodes_delimiter(input_nodes, "**", TextType.BOLD)

    def test_split_nodes_delimiter5(self):
        input_nodes = [
            TextNode("*italic text*", TextType.TEXT),
        ]
        output_nodes = [
            TextNode("italic text", TextType.ITALIC),
        ]
        delimited_by_italic = split_nodes_delimiter(input_nodes, "*", TextType.ITALIC)
        self.assertEqual(delimited_by_italic, output_nodes)

