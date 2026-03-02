import unittest
from block_to_block_type import block_to_block_type
from blocktype import BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_not_heading_missing_space(self):
        block = "#Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> quote line 1\n>quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list_valid(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_not_incrementing(self):
        block = "1. one\n3. two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_default(self):
        block = "Just a normal paragraph.\nWith two lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
