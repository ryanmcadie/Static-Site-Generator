import os
from generate_page import generate_page


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isdir(entry_path):
            # Mirror directory in dest
            new_dest_dir = os.path.join(dest_dir_path, entry)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, new_dest_dir)
        else:
            # Only generate from .md files
            if not entry.endswith(".md"):
                continue

            from_path = entry_path
            dest_filename = entry[:-3] + ".html"   # replace .md with .html
            dest_path = os.path.join(dest_dir_path, dest_filename)

            generate_page(from_path, template_path, dest_path)
