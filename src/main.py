import os
import shutil

from copystatic import copy_files_recursive
from genpage import generate_page


dir_path_static = "./static"
dir_path_public = "./public"


def main():
    print(f"Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print(f"Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    print(f"Copying files complete.")

    generate_page("./content/index.md", "./template.html", "./public/index.html")


main()
