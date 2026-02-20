from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        self.tag = tag
        self.value = value
        self.props = props
        self.props_string = ""
        # super().__init__()
        # super(LeafNode, self).__init__()

    def to_html(self):
        if self.value is None:
            raise ValueError
        if not self.tag:
            return f"{self.value}"
        self.props_string = super().props_to_html()
        return f"<{self.tag}{self.props_string}>{self.value}</{self.tag}>"

    def __repr__(self):
        if self.props:
            return f"LeafNode({self.tag}, {self.value}, {self.props})"
        else:
            return f"LeafNode({self.tag}, {self.value})"
