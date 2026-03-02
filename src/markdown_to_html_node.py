from blocktype import BlockType
from block_to_block_type import block_to_block_type
from markdown_to_blocks import markdown_to_blocks

from htmlnode import ParentNode
from htmlnode import LeafNode

from text_to_textnodes import text_to_textnodes
from htmlnode import text_node_to_html_node  # rename if your file differs


def text_to_children(text: str):
    """
    Convert inline-markdown text into a list of HTMLNodes (LeafNodes).
    """
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def paragraph_block_to_html(block: str):
    # Strip each line, then join with single spaces
    lines = block.split("\n")
    text = " ".join(line.strip() for line in lines)
    return ParentNode("p", text_to_children(text))



def heading_block_to_html(block: str):
    # block starts with 1-6 # then space then text
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1
    level = i  # 1..6
    text = block[level + 1 :]  # skip "#... " (hashes + space)
    return ParentNode(f"h{level}", text_to_children(text))


def code_block_to_html(block: str):
    inner = block[4:-3]  # remove ```\n and trailing ```
    lines = inner.split("\n")

    # Remove leading/trailing empty lines introduced by triple-quoted formatting
    while lines and lines[0].strip() == "":
        lines.pop(0)
    while lines and lines[-1].strip() == "":
        lines.pop()

    # Dedent shared indentation (same as before)
    indents = []
    for ln in lines:
        if ln.strip() == "":
            continue
        indents.append(len(ln) - len(ln.lstrip(" ")))
    trim = min(indents) if indents else 0

    dedented = "\n".join(ln[trim:] for ln in lines)

    # Ensure exactly ONE trailing newline
    dedented = dedented + "\n"

    code = LeafNode("code", dedented)
    return ParentNode("pre", [code])




def quote_block_to_html(block: str):
    lines = block.split("\n")
    stripped_lines = []

    for line in lines:
        line = line.lstrip()          # important
        if not line.startswith(">"):
            raise ValueError("Invalid quote block: line missing '>'")

        line = line[1:]               # remove >
        if line.startswith(" "):      # optional single space
            line = line[1:]

        stripped_lines.append(line)

    text = " ".join(stripped_lines)
    return ParentNode("blockquote", text_to_children(text))



def ul_block_to_html(block: str):
    lines = block.split("\n")
    items = []

    for line in lines:
        line = line.lstrip()      # <-- THIS is where it goes
        item_text = line[2:]      # after "- "
        items.append(ParentNode("li", text_to_children(item_text)))

    return ParentNode("ul", items)


def ol_block_to_html(block: str):
    lines = block.split("\n")
    items = []
    for line in lines:
        # line starts with "N. "
        # Split once on ". "
        _, item_text = line.split(". ", 1)
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", items)


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.PARAGRAPH:
            children.append(paragraph_block_to_html(block))
        elif btype == BlockType.HEADING:
            children.append(heading_block_to_html(block))
        elif btype == BlockType.CODE:
            children.append(code_block_to_html(block))
        elif btype == BlockType.QUOTE:
            children.append(quote_block_to_html(block))
        elif btype == BlockType.UNORDERED_LIST:
            children.append(ul_block_to_html(block))
        elif btype == BlockType.ORDERED_LIST:
            children.append(ol_block_to_html(block))
        else:
            raise ValueError(f"Unknown block type: {btype}")

    return ParentNode("div", children)
