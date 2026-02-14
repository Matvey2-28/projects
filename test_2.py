import unittest

def is_palindrome(a):
    b = ''.join(a).lower
    c = b.replace(' ', '')
    if c != c[::-1]:
        raise ValueError('Это не палиндром')
    return print("Это палиндром")

class Is_Palindrome(unittest.TestCase):
    def test(self):
        self.assertTrue(is_palindrome('А роза упала на азора'))
        self.assertFalse(is_palindrome('А роза упала на бориса'))
    
if __name__ == '__main__':
    unittest.main()