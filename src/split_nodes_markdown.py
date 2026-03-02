import re
from textnode import TextNode, TextType

# Reusable patterns:
# image: ![alt](url)
_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
# link (not image): [text](url) where the [ isn't preceded by !
_LINK_RE = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)')  # negative lookbehind [web:115]


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = list(_IMAGE_RE.finditer(text))  # non-overlapping matches [web:118]
        if not matches:
            new_nodes.append(node)
            continue

        last_idx = 0
        for m in matches:
            start, end = m.span()
            alt, url = m.group(1), m.group(2)

            if start > last_idx:
                new_nodes.append(TextNode(text[last_idx:start], TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            last_idx = end

        if last_idx < len(text):
            new_nodes.append(TextNode(text[last_idx:], TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = list(_LINK_RE.finditer(text))  # non-overlapping matches [web:118]
        if not matches:
            new_nodes.append(node)
            continue

        last_idx = 0
        for m in matches:
            start, end = m.span()
            anchor, url = m.group(1), m.group(2)

            if start > last_idx:
                new_nodes.append(TextNode(text[last_idx:start], TextType.TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            last_idx = end

        if last_idx < len(text):
            new_nodes.append(TextNode(text[last_idx:], TextType.TEXT))

    return new_nodes
