from textnode import TextNode, TextType


def main():
    link = TextType("link")
    tn = TextNode("This is some anchor text", link, "https://www.boot.dev")

    print(tn)


main()
