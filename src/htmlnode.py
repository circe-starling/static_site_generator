class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        self.props_string = ""

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        if len(self.props_string) == 0:
            for k in self.props.keys():
                self.props_string += f' {k}="{self.props[k]}"'
        return self.props_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        tag = self.tag == other.tag
        value = self.value == other.value
        children = self.children == other.children
        props = self.props == other.props
        if tag and value and children and props:
            return True
        else:
            return False
