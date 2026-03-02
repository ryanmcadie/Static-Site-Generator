import unittest
from textnode import TextNode, TextType
from split_nodes_markdown import split_nodes_image, split_nodes_link


class TestSplitNodesMarkdown(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_none_found(self):
        node = TextNode("No images here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_links_example(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_links_none_found(self):
        node = TextNode("No links here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links_does_not_split_images(self):
        node = TextNode(
            "An image ![alt](img.png) and a link [x](y.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # link splitter should leave the image markdown intact as TEXT
        self.assertListEqual(
            [
                TextNode("An image ![alt](img.png) and a link ", TextType.TEXT),
                TextNode("x", TextType.LINK, "y.com"),
            ],
            new_nodes,
        )

    def test_non_text_nodes_pass_through(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
            TextNode("already link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(nodes, split_nodes_image(nodes))
        self.assertListEqual(nodes, split_nodes_link(nodes))


if __name__ == "__main__":
    unittest.main()
