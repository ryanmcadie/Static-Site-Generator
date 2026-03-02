import os
import shutil


def copy_static(src_dir: str, dest_dir: str):
    # Delete destination directory contents (clean build)
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)  # deletes directory tree [web:163]
    os.mkdir(dest_dir)  # make fresh destination [web:168]

    # Recursively copy
    for entry in os.listdir(src_dir):  # list entries in src [web:168]
        src_path = os.path.join(src_dir, entry)   # build full path [web:177]
        dest_path = os.path.join(dest_dir, entry) # build full path [web:177]

        if os.path.isfile(src_path):  # file? [web:174]
            print(f"copy file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)      # copy file [web:163]
        else:
            print(f"copy dir:  {src_path} -> {dest_path}")
            copy_static(src_path, dest_path)      # recurse
