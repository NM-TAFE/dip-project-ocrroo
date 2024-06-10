import os
import unittest

from app.code_identifier import CodeIdentifier


class CodeIdentifierTestCase(unittest.TestCase):

    def setUp(self):
        self.code_identifier = CodeIdentifier("../app/code_identifier_dataset.csv")

    def test_text_oscar_wilde(self):
        text_the_picture_of_dorian_gray = ("The studio was filled with the rich odor of roses, and when the light "
                                           "summer wind stirred amidst the trees of the garden, there came through "
                                           "the open door the heavy scent of the lilac, or the more delicate perfume "
                                           "of the pink-flowering thorn.")
        detected = self.code_identifier.identify(text_the_picture_of_dorian_gray)

        self.assertEqual("Plain Text", detected)

    def test_python_class(self):
        text_python_class = "class CodeIdentifierTestCase(unittest.TestCase):"

        detected = self.code_identifier.identify(text_python_class)

        self.assertEqual("Python", detected)

    def test_empty_string(self):
        empty_string = ""
        detected = self.code_identifier.identify(empty_string)
        self.assertEqual("Plain Text", detected)

    def test_html_code(self):
        html_code = "<main><article><section>Title</section></article></main>"
        detected = self.code_identifier.identify(html_code)
        self.assertEqual("Plain Text", detected)

    def test_javascript_code(self):
        javascript_code = "function greet() { console.log('Hello, world!'); }"
        detected = self.code_identifier.identify(javascript_code)
        self.assertEqual("Plain Text", detected)

    def test_python_function(self):
        python_function = "def add(a, b):\n    return a + b"
        detected = self.code_identifier.identify(python_function)
        self.assertEqual("Python", detected)

    def test_plain_text_with_code_words(self):
        plain_text_with_code_words = "I enjoy coding but I need some holidays for sure."
        detected = self.code_identifier.identify(plain_text_with_code_words)
        self.assertEqual("Plain Text", detected)

    def test_mixed_code_and_text(self):
        mixed_code_and_text = ("Some python test you asked, have it: def add(a, b): return a + b. "
                               "Isn't it great?")
        detected = self.code_identifier.identify(mixed_code_and_text)
        self.assertEqual("Python", detected)

    def test_multiline_python_code(self):
        multiline_python_code = ("def multiply(a, b):\n"
                                 "    result = a * b\n"
                                 "    return result\n"
                                 "\n"
                                 "print(multiply(2, 3))")
        detected = self.code_identifier.identify(multiline_python_code)
        self.assertEqual("Python", detected)


if __name__ == '__main__':
    unittest.main()
