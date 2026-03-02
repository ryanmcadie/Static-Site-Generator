import re
from blocktype import BlockType

def block_to_block_type(block: str) -> BlockType:
    # Heading: 1-6 #'s then a space
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING

    # Code: starts with ```\n and ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # Quote: every line starts with ">" (allow indentation)
    if all(line.lstrip().startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- " (allow indentation)
    if all(line.lstrip().startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: must be 1., 2., 3. ... (allow indentation)
    ordered_ok = True
    for i, line in enumerate(lines, start=1):
        if not line.lstrip().startswith(f"{i}. "):
            ordered_ok = False
            break
    if ordered_ok:
        return BlockType.ORDERED_LIST

    # IMPORTANT: default case
    return BlockType.PARAGRAPH
