import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        md = (
            "# This is a heading\n\n"
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n"
            "- This is the first list item in a list block\n"
            "- This is a list item\n"
            "- This is another list item\n"
        )
        blocks = markdown_to_blocks(md)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
            blocks,
        )

    def test_strips_and_removes_empty_blocks(self):
        md = "\n\n  # Heading  \n\n\n\n   \n\nParagraph\n\n"
        blocks = markdown_to_blocks(md)
        self.assertListEqual(["# Heading", "Paragraph"], blocks)

    def test_single_block(self):
        md = "Just one block"
        self.assertListEqual(["Just one block"], markdown_to_blocks(md))


if __name__ == "__main__":
    unittest.main()
