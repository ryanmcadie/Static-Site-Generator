import os

from markdown_to_html_node import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_content = markdown_to_html_node(md).to_html()
    title = extract_title(md)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Basepath replacements (only for root-relative links)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)  # [web:189]

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)
