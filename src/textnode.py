import re
from enum import Enum

from src.leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    UNDERLINE = "underline"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        text = self.text == other.text
        text_type = self.text_type == other.text_type
        url = self.url == other.url
        if text and text_type and url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            atoms = node.text.split(delimiter, maxsplit=2)
            if len(atoms) < 2:
                raise Exception("No delimiter found")
            if len(atoms) == 2:
                raise Exception("Matching closing delimiter not found")
            else:
                new_nodes.append(TextNode(atoms[0], TextType.TEXT))
                new_nodes.append(TextNode(atoms[1], text_type))
                new_nodes.append(TextNode(atoms[2], TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    # Return sample: [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    # Return sample: [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        this_text = node.text
        imgs = extract_markdown_images(this_text)
        if len(imgs) == 0:
            return [old_nodes]
        for img in imgs:
            sections = this_text.split(f"![{img[0]}]({img[1]})", 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
            this_text = sections[1]
        if len(this_text) > 0:
            new_nodes.append(TextNode(this_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        this_text = node.text
        links = extract_markdown_links(this_text)
        if len(links) == 0:
            return [old_nodes]
        for link in links:
            sections = this_text.split(f"[{link[0]}]({link[1]})", 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            this_text = sections[1]
        if len(this_text) > 0:
            new_nodes.append(TextNode(this_text, TextType.TEXT))
    return new_nodes
