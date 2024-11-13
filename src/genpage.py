def extract_title(markdown):
    header = markdown.split("\n", 1)[0]
    if not header.startswith("# "):
        raise Exception("Markdown doesnt start with a h1 header")
    return header.strip("# ")
