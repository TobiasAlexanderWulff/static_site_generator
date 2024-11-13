import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    header = markdown.split("\n", 1)[0]
    if not header.startswith("# "):
        raise Exception("Markdown doesnt start with a h1 header")
    return header.strip("# ")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, "r").read()
    template = open(template_path, "r").read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    open(dest_path, "w").write(content)
            
