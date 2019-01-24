'''
Created on 24/1/2019

@author: arcano
'''
import unittest

from server import operate

class TestServer(unittest.TestCase):

    def testOperate(self):
        self.assertEqual(operate("41 / 50 + 53 + 40"), 93 )
        self.assertEqual(operate("38 - 83 - 52 + 30 - 24 - 89 / 66 + 18 / 7 * 77"), 62 )
        self.assertEqual(operate("57 + 87 - 24 * 27 / 8 + 53 - 87 * 6 * 60 - 30"), -31234 )
        self.assertEqual(operate("63 * 23 - 91 - 17 * 45 + 63 * 52 - 50"), 3819 )
        self.assertEqual(operate("47 - 88 + 32 - 71 * 39 * 68"), -188301 )
        self.assertEqual(operate("43 * 47 - 75 + 94 * 35 - 60 + 55 + 8"), 5239 )
        self.assertEqual(operate("0 + 0"), 0)


if __name__ == "__main__":
    unittest.main()