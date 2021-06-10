# Importing unittest to test InputCheck class.
import unittest
# Also, importing InputCheck class as itself.
from timeSoft_test import InputCheck


class TestInputCheck(unittest.TestCase):
    """This class implements testing of InputCheck class from timeSoft.py file."""

    def setUp(self):
        # Setting up a reference to a InputCheck class.
        # In the next methods, using indexing for returning boolean type only.
        self.check = InputCheck

    def test_email_InputCheck(self):
        # Cheking if check_email() returns True when it takes a correct arg.
        self.assertTrue(self.check('tlastivka@ex.ua').check_email())
        # Making a few various tests:
        # Checking if check_email() returns False when it takes a incorrect args.
        self.assertFalse(self.check('tlastivka@@ex.ua').check_email()[0])
        self.assertFalse(self.check('tlastivka@ex..ua').check_email()[0])
        self.assertFalse(self.check('tlastivka/@ex.ua').check_email()[0])
        self.assertFalse(self.check('!tlastivka@ex..ua').check_email()[0])

    def test_incorrect_InputCheck(self):
        # Cheking if check_incorrect_vals() returns True when it takes a correct arg.
        self.assertTrue(self.check('Hello World').check_incorrect_vals())
        # Making a few various tests:
        # Cheking if check_incorrect_vals() returns False when it takes a incorrect args.
        self.assertFalse(self.check(',').check_incorrect_vals()[0])
        self.assertFalse(self.check('\\').check_incorrect_vals()[0])
        self.assertFalse(self.check('/').check_incorrect_vals()[0])
        self.assertFalse(self.check('"').check_incorrect_vals()[0])

    def test_spaces_tabs_InputCheck(self):
        # Cheking if check_spaces_tabs() returns True when it takes a correct arg.
        self.assertTrue(self.check('HelloWorld').check_spaces_tabs())
        # Making a few various tests:
        # Cheking if check_spaces_tabs() returns False when it takes a incorrect args.
        self.assertFalse(self.check(' ').check_spaces_tabs()[0])
        self.assertFalse(self.check('    ').check_spaces_tabs()[0])

    def test_number_only_InputCheck(self):
        # Cheking if number_only() returns True when it takes a correct arg.
        self.assertTrue(self.check('0').number_only())
        # Making a few various tests:
        # Cheking if number_only() returns False when it takes a incorrect args.
        self.assertFalse(self.check('Hello0World!').number_only()[0])


if __name__ == '__main__':
    unittest.main()
