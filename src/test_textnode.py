import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("test node", TextType.BOLD)
        node2 = TextNode("test node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("test node", TextType.BOLD, "https://www.test.org")
        node2 = TextNode("test node", TextType.BOLD, "https://www.test.org")
        self.assertEqual(node, node2)
    
    def test_eq3(self):
        node = TextNode("test node", TextType.BOLD)
        node2 = TextNode("test node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_non_eq(self):
        node = TextNode("test node", TextType.BOLD)
        node2 = TextNode("test node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_non_eq2(self):
        node = TextNode("test node", TextType.BOLD)
        node2 = TextNode("different test node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_non_eq3(self):
        node = TextNode("test node", TextType.BOLD, "https://www.test.org")
        node2 = TextNode("test node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_non_eq4(self):
        node = TextNode("test node", TextType.BOLD, "https://www.test.org")
        node2 = TextNode("different test node", TextType.BOLD, "https://www.other.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
