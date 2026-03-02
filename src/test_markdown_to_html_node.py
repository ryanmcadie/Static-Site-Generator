import unittest
from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
            md = "# Hello"
            node = markdown_to_html_node(md)
            self.assertEqual(node.to_html(), "<div><h1>Hello</h1></div>")

    def test_ul(self):
            md = """
    - one
    - **two**
    - three
    """
            node = markdown_to_html_node(md)
            self.assertEqual(
                node.to_html(),
                "<div><ul><li>one</li><li><b>two</b></li><li>three</li></ul></div>",
            )

    def test_quote(self):
            md = """
    > quote line one
    > quote line **two**
    """
            node = markdown_to_html_node(md)
            self.assertEqual(
                node.to_html(),
                "<div><blockquote>quote line one quote line <b>two</b></blockquote></div>",
            )


if __name__ == "__main__":
    unittest.main()