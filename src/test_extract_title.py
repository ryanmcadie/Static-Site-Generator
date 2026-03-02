import unittest
from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello   "), "Hello")

    def test_extract_title_raises_if_missing(self):
        with self.assertRaises(ValueError):
            extract_title("## Not h1\nJust text")


if __name__ == "__main__":
    unittest.main()
