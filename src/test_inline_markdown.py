import unittest

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        input = TextNode("This is text with a **bolded** word", TextType.TEXT)    
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(output, expected)

    def test_delim_bold_double(self):
        input = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
        ]
        self.assertListEqual(output, expected)
    
    def test_delim_bold_multiword(self):
        input = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded word", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another", TextType.BOLD),
        ]
        self.assertListEqual(output, expected)

    def test_delim_italic(self):
        input = TextNode("This is text with an *italic* word", TextType.TEXT)
        output = split_nodes_delimiter([input], "*", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(output, expected)

    def test_delim_bold_and_italic(self):
        input = TextNode("**bold** and *italic*", TextType.TEXT)
        output = split_nodes_delimiter([input], "**", TextType.BOLD)
        output = split_nodes_delimiter(output, "*", TextType.ITALIC)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(output, expected)

    def test_delim_code(self):
        input = TextNode("This is text with a `code block` word", TextType.TEXT)
        output = split_nodes_delimiter([input], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(output, expected)

    def test_extract_markdown_images(self):
        input = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        output = extract_markdown_images(input)
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(output, expected)

    def test_extract_markdown_links(self):
        input = "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        output = extract_markdown_links(input)
        expected = [
            ("link", "https://boot.dev"),
            ("another link", "https://blog.boot.dev"),
        ]
        self.assertListEqual(output, expected)

    def test_split_image(self):
        input = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        output = split_nodes_image([input])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(output, expected)

    def test_split_image_single(self):
        input = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        output = split_nodes_image([input])
        expected = [TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG")]
        self.assertListEqual(output, expected)

    def test_split_images(self):
        input = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        output = split_nodes_image([input])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(output, expected)

    def test_split_links(self):
        input = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        output = split_nodes_link([input])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
            TextNode(" with text that follows", TextType.TEXT),
        ]
        self.assertListEqual(output, expected)

    def test_text_to_textnodes(self):
        input = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        output = text_to_textnodes(input)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(output, expected)


if __name__ == "__main__":
    unittest.main()

