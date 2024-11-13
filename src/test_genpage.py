import unittest

from genpage import extract_title


class TestGenpage(unittest.TestCase):
    def test_extract_title(self):
        markdown = """# Title

some text
"""
        output = extract_title(markdown)
        expected = "Title"
        self.assertEqual(output, expected)
    
    def test_extract_title_fail(self):
        markdown = """
This is just some test with no h1 heading
"""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_extract_title_fail_because_wrong_heading_level(self):
        markdown = """### h3 heading

some text
"""
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
