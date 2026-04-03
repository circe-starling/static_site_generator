import unittest

from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)


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

    ##################################################
    ####### new after writing text_node_to_html_node()
    ##################################################

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_to_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_text_to_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    #### code
    def test_text_to_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    #### link
    def test_text_to_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    #### image
    def test_text_to_img(self):
        node = TextNode("This is image alt text", TextType.IMAGE, "images/balloon.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(
            html_node.props,
            {"src": "images/balloon.jpg", "alt": "This is image alt text"},
        )

    ##################################################
    ####### new after writing split_nodes_delimiter()
    ##################################################

    def test_splitnodes_bold(self):
        text = "This is text with a **bolded** word."
        split_text = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded", TextType.BOLD),
            TextNode(" word.", TextType.TEXT),
        ]
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, split_text)

    def test_splitnodes_italic(self):
        text = "This is text with an *italicized* word."
        split_text = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
        ]
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, split_text)

    def test_splitnodes_multiplenodes(self):
        text1 = "This is text with an *italicized* word."
        split_text1 = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
        ]
        node1 = TextNode(text1, TextType.TEXT)

        text2 = "This is text with another *italicized* word."
        split_text2 = [
            TextNode("This is text with another ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
        ]
        node2 = TextNode(text2, TextType.TEXT)

        split_text1.extend(split_text2)
        new_nodes = split_nodes_delimiter([node1, node2], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, split_text1)

    def test_wrong_delimiter(self):
        text = "This is text with a `code block` in it."
        split_text = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in it.", TextType.TEXT),
        ]
        node = TextNode(text, TextType.TEXT)
        ## The following commented-out line throws an error, as it should
        # new_nodes = split_nodes_delimiter([node], "**", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, split_text)

    ###########################################################
    ####### new after writing image and link extracting regexes
    ###########################################################

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_bad_syntax(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "Two images ![image1](image1.jpg) and ![image2](image2.bmp)"
        )
        self.assertListEqual(
            [("image1", "image1.jpg"), ("image2", "image2.bmp")], matches
        )

    ##-----------> now write functions for extracting links
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link to a webpage](https://www.webpage.web)"
        )
        self.assertListEqual(
            [("link to a webpage", "https://www.webpage.web")], matches
        )

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "Two links are [link1](www.link1.com) and [link2](www.link2.com)"
        )
        self.assertListEqual(
            [("link1", "www.link1.com"), ("link2", "www.link2.com")], matches
        )

    ##################################################################
    ####### new after writing function to split text by images & links
    ##################################################################

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](http://www.w.co) and another [2nd link](http://www.i.co) here",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "http://www.w.co"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("2nd link", TextType.LINK, "http://www.i.co"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
