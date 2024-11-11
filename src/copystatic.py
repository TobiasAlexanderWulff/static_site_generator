import os
import shutil


def copy_files_recursive(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for file_name in os.listdir(src):
        current_src_path = os.path.join(src, file_name)
        current_dst_path = os.path.join(dst, file_name)
        print(f"* {current_src_path} -> {current_dst_path}")
        if os.path.isfile(current_src_path):
            shutil.copy(current_src_path, dst)
        else:
            copy_files_recursive(current_src_path, current_dst_path)
