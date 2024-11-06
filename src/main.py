from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode


def main():
    textnode = TextNode("test text", TextType.ITALIC)
    print(textnode)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
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


if __name__=="__main__":
    main()
