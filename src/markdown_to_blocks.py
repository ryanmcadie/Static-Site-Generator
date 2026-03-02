def markdown_to_blocks(markdown: str) -> list[str]:
    # Split on blank lines (double newline)
    raw_blocks = markdown.split("\n\n")
    # Strip whitespace and drop empties
    blocks = [b.strip() for b in raw_blocks if b.strip() != ""]
    return blocks
