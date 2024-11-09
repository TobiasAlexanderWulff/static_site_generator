import re

from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode


def main():
    return


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
        remaining_text = old_node.text
        for image in images:
            image_alt, image_url = image
            splitted = remaining_text.split(f"![{image_alt}]({image_url})", 1)
            new_nodes.append(TextNode(splitted[0], old_node.text_type, url=old_node.url))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, url=image_url))
            remaining_text = splitted[1]
        new_nodes.append(TextNode(remaining_text, old_node.text_type, url=old_node.url))

    return list(filter(lambda node: node.text != "", new_nodes))


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        remaining_text = old_node.text
        for link in links:
            link_text, link_url = link
            splitted = remaining_text.split(f"[{link_text}]({link_url})", 1)
            new_nodes.append(TextNode(splitted[0], old_node.text_type, url=old_node.url))
            new_nodes.append(TextNode(link_text, TextType.LINK, url=link_url))
            remaining_text = splitted[1]
        new_nodes.append(TextNode(remaining_text, old_node.text_type, url=old_node.url))

    return list(filter(lambda node: node.text != "", new_nodes))


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(markdown):
    blocks = list(map(lambda block: block.strip(), markdown.split("\n\n")))
    return list(filter(lambda block: block != "", blocks))


def block_to_block_type(block):
    if re.fullmatch(r"^#{1,6}\s.+", block):
        return "heading"
    if re.fullmatch(r"^`{3}[^`]+`{3}$", block):
        return "code"
    
    lines = block.split("\n")
    match = True
    for line in lines:
        if not re.match(r"^>.+", block):
            match = False
    if match:
        return "quote"
        
    match = True
    for line in lines:
        if not re.match(r"^[\*-]\s.+", line):
            match = False
            break
    if match:
        return "unordered_list"

    match = True
    for i, line in enumerate(lines):
        if not re.match(rf"^{i+1}\.\s.+", line):
            match = False
            break
    if match:
        return "ordered_list"
    
    return "paragraph"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        html_nodes.append(block_to_html_node(type, block))
    return ParentNode("div", html_nodes)


def block_to_html_node(type, block):
    match type:
        case "heading":
            level, text = block.split(" ", 1)
            return ParentNode(f"h{len(level)}", text_to_children(text))
        case "code":
            text = block.strip("`")
            return ParentNode("pre", [ParentNode("code", text_to_children(text))])
        case "quote":
            block = block[2:]
            if block[0] == ">":
                children = [block_to_html_node("quote", block)]
            else:
                children = text_to_children(block.replace("> ", ""))
            return ParentNode("blockquote", children)
        case "unordered_list":
            children = list(map(lambda line: ParentNode("li", text_to_children(line[2:])), block.split("\n")))
            return ParentNode("ul", children)
        case "ordered_list":
            children = list(map(lambda line: ParentNode("li", text_to_children(line.split(" ", 1)[1])), block.split("\n")))
            return ParentNode("ol", children)
        case "paragraph":
            return ParentNode("p", text_to_children(block))
        

def text_to_children(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))


if __name__=="__main__":
    main()
    result = markdown_to_html_node("""
# This is a Heading

This is a simple paragraph.

> This is a quote.
> With second line.

> > This is a second level quote.

```
This is inside a code block.
```

## This is a different header             

This is a paragraph with some **bold** and *italic* text inside.
And this is a paragraph with some ```code``` embedded.
Also this is a paragraph with an ![image](https://www.test.org/image.png).
And this has a [link](https://www.website.de/site#1) embedded.


- This is a list
- :)
* Hey :D

1. This
2. list
3. is
4. ordered.
""")
    print(result.to_html())
