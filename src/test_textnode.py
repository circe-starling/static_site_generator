import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ineq_text(self):
        node3 = TextNode("Text node text node", TextType.ITALIC, None)
        node4 = TextNode("Node text node text", TextType.ITALIC, None)
        self.assertNotEqual(node3, node4)

    def test_ineq_link(self):
        node5 = TextNode("This is a text node", TextType.UNDERLINE, "www.boot.dev")
        node6 = TextNode("This is a text node", TextType.UNDERLINE)
        self.assertNotEqual(node5, node6)

    def test_ineq_texttype(self):
        node7 = TextNode("Text node, this is", TextType.BOLD)
        node8 = TextNode("Text node, this is", TextType.ITALIC)
        self.assertNotEqual(node7, node8)


if __name__ == "__main__":
    unittest.main()
