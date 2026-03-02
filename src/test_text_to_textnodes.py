import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_full_example(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_plain_text(self):
        text = "Just normal text"
        expected = [TextNode("Just normal text", TextType.TEXT)]
        self.assertListEqual(expected, text_to_textnodes(text))

    def test_only_link_and_image(self):
        text = "![a](img.png) and [b](url.com)"
        expected = [
            TextNode("a", TextType.IMAGE, "img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.LINK, "url.com"),
        ]
        self.assertListEqual(expected, text_to_textnodes(text))


if __name__ == "__main__":
    unittest.main()
