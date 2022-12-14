import unittest
from name_function import get_formatted_name

class NamesTestCase(unittest.TestCase):
    """name_function.py 테스트"""

    def test_first_last_name(self):
        """'Janis Joplin' 같은 이름이 동작하는지?"""
        formatted_name = get_formatted_name('janis', 'joplin')
        self.assertEqual(formatted_name, 'Janis Joplin')

    def test_first_last_middle_name(self):
        """'Wolfgang Amadeus Mozart' 같은 이름이 동작하는지?"""
        formatted_name = get_formatted_name('wolfgang', 'mozart', 'amadeus')
        self.assertEqual(formatted_name, 'Wolfgang Amadeus Mozart')

if __name__ == '__main__':
    unittest.main()