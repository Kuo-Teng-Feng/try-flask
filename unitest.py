import unittest
from inicancelpath import randomizer

class test_randomizer(unittest.TestCase):    
    # n-digit.
    def test_randomizer_4(self): # prefix "test_" is necessary.      
        self.assertEqual(len(randomizer(4)), 4)
    
    def test_randomizer_30(self): 
        self.assertEqual(len(randomizer(30)), 30)
        
    def test_randomizer_62(self): 
        self.assertEqual(len(randomizer(62)), 62)
    
    def test_randomizer_99(self): 
        self.assertEqual(len(randomizer(99)), 99)
        
    def test_randomizer_999(self): 
        self.assertEqual(len(randomizer(999)), 999)
    
if __name__ == "__main__":
    unittest.main()