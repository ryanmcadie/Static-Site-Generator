from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        parts = text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Unclosed '{delimiter}' delimiter in text: {text}")
        
        # Include ALL parts, even empty ones
        for i in range(len(parts)):
            if i % 2 == 0:
                # Even indices = TEXT
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                # Odd indices = new text_type
                new_nodes.append(TextNode(parts[i], text_type))
    
    return new_nodes
