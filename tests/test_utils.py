import unittest
from utils.validators import validate_score, validate_not_empty,validate_name

class TestUtils(unittest.TestCase):

    def test_validate_score(self):
        valid, val=validate_score(85)
        self.assertTrue(valid)
        self.assertEqual(val, 85.0)

        valid, val=validate_score(150)
        self.assertFalse(valid)

    def test_validtae_not_empty(self):
        self.assertTrue(validate_not_empty("Hello"))
        self.assertFalse(validate_not_empty(" "))

    def test_validate_name(self):
        self.assertTrue(validate_name("Alice-Johnson"))
        self.assertFalse(validate_name("Alice123"))
        