import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    
    def test_to_html2(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                ParentNode(
                    "div",
                    [
                        LeafNode("a", "link text", props={"href": "https://www.google.com"}),
                        LeafNode("h1", "heading 1 text"),
                    ],
                    props={
                        "class": "cool_div",
                    }
                ),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i><div class="cool_div"><a href="https://www.google.com">link text</a><h1>heading 1 text</h1></div></p>')

    def test_to_html3(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertRaises(ValueError, node.to_html)

    def test_to_html4(self):
        node = ParentNode(
            "div",
            [],
        )
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html5(self):
        node = ParentNode(
            "div",
            None,
        )
        self.assertRaises(ValueError, node.to_html)
