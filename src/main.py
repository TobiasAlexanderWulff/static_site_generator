from textnode import TextNode, NodeType

def main():
    textnode = TextNode("test text", NodeType.ITALIC, "https://www.boot.dev")
    print(textnode)

main()
