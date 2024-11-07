import re

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode


def main():
    textnode = TextNode("test text", TextType.ITALIC)
    print(textnode)


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url,})
        case TextType.IMAGE:
            return LeafNode("img", None, props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("unknown text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            splitted = old_node.text.split(delimiter)
            if len(splitted) > 1 and len(splitted) % 2 != 1:
                raise Exception("Invalid Markdown syntax: matching closing delimiter not found")
            for i in range(len(splitted)):
                if splitted[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(splitted[i], old_node.text_type))
                else:
                    new_nodes.append(TextNode(splitted[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
        remaining_text = old_node.text
        for image in images:
            image_alt, image_url = image
            splitted = remaining_text.split(f"![{image_alt}]({image_url})", 1)
            new_nodes.append(TextNode(splitted[0], old_node.text_type))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_url))
            remaining_text = splitted[1]
        new_nodes.append(TextNode(remaining_text, old_node.text_type))

    return list(filter(lambda node: node.text != "", new_nodes))


def split_nodes_links(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
        remaining_text = old_node.text
        for link in links:
            link_text, link_url = link
            splitted = remaining_text.split(f"[{link_text}]({link_url})", 1)
            new_nodes.append(TextNode(splitted[0], old_node.text_type))
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
            remaining_text = splitted[1]
        new_nodes.append(TextNode(remaining_text, old_node.text_type))

    return list(filter(lambda node: node.text != "", new_nodes))


if __name__=="__main__":
    main()
    
