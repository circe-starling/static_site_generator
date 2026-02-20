from enum import Enum


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


class TextType(Enum):
    LINK = "link"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
