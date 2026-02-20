import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_eq(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)

    def test_eq(self):
        node3 = HTMLNode("p", "This is a paragraph.", props={"id": "lead"})
        node4 = HTMLNode("p", "This is a paragraph.", props={"id": "lead"})
        self.assertEqual(node3, node4)

    def test_ineq_props(self):
        node5 = HTMLNode(
            "a", "This is a link.", props={"href": "www.boot.dev", "id": "lead"}
        )
        # node5_props = node5.props_to_html()
        node6 = HTMLNode(
            "a", "This is a link.", props={"href": "www.boot.dev", "id": "body"}
        )
        # node6_props = node6.props_to_html()
        # print(f"Node5 properties: {node5_props}")
        # print(f"Node6 properties: {node6_props}")
        self.assertNotEqual(node5, node6)

    def test_ineq_tags(self):
        node7 = HTMLNode("p", "This is a paragraph.")
        node8 = HTMLNode("span", "This is a paragraph.")
        self.assertNotEqual(node7, node8)

    def test_ineq_value(self):
        node9 = HTMLNode("p", "This is a paragraph.")
        node10 = HTMLNode("p", "This is another paragraph.")
        self.assertNotEqual(node9, node10)


if __name__ == "__main__":
    unittest.main()
