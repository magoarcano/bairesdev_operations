'''
Created on 24/1/2019

@author: arcano
'''
import unittest

from mpserver import OperationProcess

from sympy import S

class TestServer(unittest.TestCase):
    expressions = ["38 - 83 - 52 + 30 - 24 - 89 / 66 + 18 / 7 * 77",
                   "57 + 87 - 24 * 27 / 8 + 53 - 87 * 6 * 60 - 30",
                   "63 * 23 - 91 - 17 * 45 + 63 * 52 - 50",
                   "47 - 88 + 32 - 71 * 39 * 68",
                   "43 * 47 - 75 + 94 * 35 - 60 + 55 + 8",
                   "49 - 97 + 17 + 31 / 37 + 82",
                   "74 - 36 - 96 + 32 + 2 + 26",
                   "43 - 45 - 66 - 52 - 6",
                   "41 / 50 + 53 + 40",
                   "40 * 76 + 97 - 90 * 52",
                   "62 - 42 + 7 - 74 / 88",
                   "66 - 11 / 5 / 58 + 18 - 58 - 88 + 97",
                   "36 / 48 * 21 - 36 + 69 + 26 + 35 + 49 + 7",
                   "58 * 10 - 19 - 59",
                   "63 / 68 * 86 - 62 - 32",
                   "23 - 90 - 8 + 40 / 50",
                   "98 * 8 - 23 + 58 + 95",
                   "46 * 11 + 57 * 35 + 96",
                   "48 - 62 - 90 - 57 + 22 + 30",
                   "5 + 93 - 16 * 97 + 70 / 76 - 60 - 5 + 73 - 5",
                   "89 * 30 / 42 * 16 + 77 - 30 / 92 + 39 + 65",
                   "42 + 23 + 75 - 90",
                   ]
        
    def testSimple(self):
        for expression in self.expressions:
            self.assertEqual(OperationProcess._operate(expression), "%d\n" % S(expression).evalf() )


if __name__ == "__main__":
    unittest.main()