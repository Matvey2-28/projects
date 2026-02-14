import unittest

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError('Деление на ноль запрещено')
    return a / b

class MyTestCase(unittest.TestCase):
    
    def test_divide(self):
        self.assertEqual(divide(6, 2), 3)
        self.assertNotEqual(divide(10, 3), 4)
        self.assertTrue(divide(15, 5) == 3)
        self.assertFalse(divide(10, 2) == 2)
        
    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)
        
if __name__ == '__main__':
    unittest.main()