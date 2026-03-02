import sys

from copy_static import copy_static
from generate_pages_recursive import generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # ensure it always ends with /
    if not basepath.endswith("/"):
        basepath += "/"

    # build into docs (GitHub Pages default)
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
