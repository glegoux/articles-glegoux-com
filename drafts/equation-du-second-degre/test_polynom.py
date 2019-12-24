#!/usr/bin/env python2
#-*- coding: UTF-8 -*-
#test_polynom.py

import unittest

from polynom import Polynom

class TestPolynom(unittest.TestCase):

    def test_a_zero(self):
        """ Coefficient a should not be 0 """
        with self.assertRaises(AssertionError):
            p = Polynom(0, 1, 2)

    def test_none_solution(self):
        """ Resolve X^2 + X + 1 = 0 """
        p = Polynom(1, 1, 1)
        self.assertEqual(str(p), 'X^2 + X + 1')
        self.assertEqual(p.get_sol(), [])

    def test_one_solution(self):
        """ Resolve X^2 = 0 """
        p = Polynom(1, 0, 0)
        self.assertEqual(str(p), 'X^2')
        self.assertEqual(p.get_sol(), [0])

    def test_two_solutions(self):
        """ Resolve X^2 - X - 12 = 0 """
        p = Polynom(1, -1, -12)
        self.assertEqual(str(p), 'X^2 - X - 12')
        self.assertEqual(p.get_sol(), [-3, 4])

if __name__ == '__main__':
    unittest.main()
