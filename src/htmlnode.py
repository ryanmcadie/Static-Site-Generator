from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html must be implemented by subclasses")  # [web:23][web:20]

    def props_to_html(self):
        if not self.props:
            return ""
        # dicts preserve insertion order in modern Python, so this will be stable for tests [web:22][web:25]
        parts = []
        for key, val in self.props.items():
            parts.append(f'{key}="{val}"')
        return " " + " ".join(parts)

    def __repr__(self):
        # Developer-focused representation including all main fields [web:21][web:27][web:30]
        return (
            f"HTMLNode(tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r})"
        )
        
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        # tag is allowed to be None, but value is required
        if value is None:
            # Using ValueError for invalid/missing value is standard practice [web:42][web:45]
            raise ValueError("LeafNode must have a non-None value")
        super().__init__(tag=tag, value=value, children=None, props=props)  # [web:34][web:44][web:38]

    def to_html(self):
        if self.value is None:
            # Extra guard, though __init__ already checks
            raise ValueError("LeafNode must have a value")  # [web:42][web:45]

        if self.tag is None:
            # Raw text, no tag wrapper
            return self.value

        # Use parent's props_to_html to build attributes string
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def __repr__(self):
        # No children in LeafNode representation
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a non-None tag")  # [web:36][web:56]
        if children is None:
            raise ValueError("ParentNode must have non-None children")  # Different message [web:36][web:56]
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        # Validation already done in __init__
        props_str = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})"
    
def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("Input must be a TextNode instance")
    
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            # This case theoretically unreachable with valid TextNode, but good practice
            raise ValueError(f"Unsupported TextType: {text_node.text_type}")