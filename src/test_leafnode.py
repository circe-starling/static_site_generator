import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node0 = LeafNode("p", "Hello, world!")
        self.assertEqual(node0.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node1 = LeafNode("a", "Here is a link!", {"href": "https://www.google.com"})
        node1_compare_text = '<a href="https://www.google.com">Here is a link!</a>'
        self.assertEqual(node1.to_html(), node1_compare_text)

    def test_leaf_to_html_ineq(self):
        node2 = LeafNode("b", "Here is some text!")
        node3 = LeafNode("i", "Here is some text!")
        self.assertNotEqual(node2.to_html(), node3.to_html())

    def test_leaf_to_html_h1(self):
        node4 = LeafNode("h1", "Heading One!")
        self.assertEqual(node4.to_html(), "<h1>Heading One!</h1>")
