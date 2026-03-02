import re

def extract_markdown_images(text):
    pattern = r'!\[([^\]]*?)\]\s*\(\s*(.*?)\s*\)'
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r'(?<!\!)\[([^\]]*?)\]\s*\(\s*(.*?)\s*\)'
    return re.findall(pattern, text)
