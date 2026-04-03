from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props
        self.props_string = ""

    def to_html(self):
        if not self.tag:
            raise ValueError("This node is missing a tag")
        if not self.children:
            raise ValueError("This node is missing its children")
        self.props_string = super().props_to_html()
        kids = ""
        for child in self.children:
            kids += child.to_html()
        return f"<{self.tag}{self.props_string}>{kids}</{self.tag}>"

    def __repr__(self):
        if self.props:
            return f"ParentNode({self.tag}, {self.children}, {self.props})"
        else:
            return f"ParentNode({self.tag}, {self.children})"

    # def __eq__(self, other):
    #     tag = self.tag == other.tag
    #     # value = self.value == other.value
    #     children = self.children == other.children
    #     props = self.props == other.props
    #     if tag and children and props:
    #         return True
    #     else:
    #         return False
