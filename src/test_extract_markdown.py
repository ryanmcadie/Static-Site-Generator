import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        text = "Text with ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_no_images(self):
        text = "Just plain text with no images"
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_markdown_links(self):
        text = "Link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_multiple_links(self):
        text = "[Google](https://google.com) [Wiki](https://wikipedia.org)"
        expected = [
            ("Google", "https://google.com"),
            ("Wiki", "https://wikipedia.org"),
        ]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_mixed_content(self):
        text = """
        Normal text ![img1](img1.png) link [here](url.com) ![img2](img2.jpg)
        """
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(len(links), 1)
        self.assertEqual(images[0][0], "img1")
        self.assertEqual(links[0][0], "here")


if __name__ == "__main__":
    unittest.main()
