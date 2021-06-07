from timeSoft_test import *
import unittest

class TestInputCheckSuccess(unittest.TestCase):
    def setUp(self):
        self.check = InputCheck
        
    # def test_email_password(self):
        # self.assertTrue(self.check('tlastivka@ex.ua').check_email())
        # self.assertFalse(self.check('qwerty').check_incorrect_vals())
        # pass

    def test_check_password_len(self):
        self.assertTrue(self.check('a').check_len())


if __name__ == '__main__':
    unittest.main()
    # print(InputCheck('a').check_len())