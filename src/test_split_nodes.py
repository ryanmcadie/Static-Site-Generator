import unittest
from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(len(new_nodes), 3)
        for i, (new, exp) in enumerate(zip(new_nodes, expected)):
            self.assertEqual(new.text, exp.text)
            self.assertEqual(new.text_type, exp.text_type)

    def test_bold_delimiter(self):
        node = TextNode("Normal **bold text** here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Normal ")
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " here")

    def test_italic_delimiter(self):
        node = TextNode("Normal _italic text_ normal", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "italic text")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_non_text_node_passes_through(self):
        nodes = [
            TextNode("text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("code", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.CODE)

    def test_unclosed_delimiter_raises(self):
        node = TextNode("Unclosed `delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_delimiter_at_end(self):
        node = TextNode("Text with**bold**end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[2].text, "end")

    def test_multiple_delimiter_steps(self):
        node = TextNode("**bold** and `code`", TextType.TEXT)
        step1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        # step1: ['', 'bold', ' and `code`']
        final = split_nodes_delimiter(step1, "`", TextType.CODE)
        # final: ['', 'bold', ' and ', 'code', '']
        self.assertEqual(len(final), 5)
        texts = [n.text for n in final]
        types = [n.text_type.name for n in final]
        self.assertEqual(texts, ['', 'bold', ' and ', 'code', ''])
        self.assertEqual(types, ['TEXT', 'BOLD', 'TEXT', 'CODE', 'TEXT'])

    def test_multiple_same_delimiters(self):
        node = TextNode("**first** then **second**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # ['', 'first', ' then ', 'second', '']
        self.assertEqual(len(new_nodes), 5)
        texts = [n.text for n in new_nodes]
        self.assertEqual(texts, ['', 'first', ' then ', 'second', ''])


if __name__ == "__main__":
    unittest.main()
