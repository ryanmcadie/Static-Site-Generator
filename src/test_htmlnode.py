import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode(
            tag="a",
            value="Click me",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="Hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="Hello", props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_repr_includes_fields(self):
        node = HTMLNode(tag="p", value="Hi", children=[], props={"class": "text"})
        rep = repr(node)
        self.assertIn("HTMLNode", rep)
        self.assertIn("tag='p'", rep)
        self.assertIn("value='Hi'", rep)
        self.assertIn("children=[]", rep)
        self.assertIn("props={'class': 'text'}", rep)
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_raw_text_when_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_raises_when_value_none(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_multiple_children_mixed_types(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode("p", children)
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_no_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_nested_parent_nodes(self):
        innermost = ParentNode("em", [LeafNode(None, "deep")])
        middle = ParentNode("strong", [LeafNode(None, "strong "), innermost])
        outer = ParentNode("p", [LeafNode(None, "Text "), middle])
        self.assertEqual(
            outer.to_html(),
            "<p>Text <strong>strong <em>deep</em></strong></p>",
        )

    def test_raises_tag_none(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "test")])

    def test_raises_children_none(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)
            
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Empty for img
        self.assertEqual(html_node.props, {"src": "image.png", "alt": "Alt text"})

    def test_invalid_input_raises(self):
        # Test non-TextNode input
        class FakeNode:
            text_type = "fake"
        
        fake_node = FakeNode()
        with self.assertRaises(ValueError):
            text_node_to_html_node(fake_node)

if __name__ == "__main__":
    unittest.main()
