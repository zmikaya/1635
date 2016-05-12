# TestUserController.py
# Assignment 3

# Author: Alessandro Lira

import unittest, math

from IllegalArgumentException import *
from FollowingController import *
from UserController import *
from Airplane import *
from Simulator import *
from Control import *

class TestUserController(unittest.TestCase):

	# Test constructor does not throw an error
	def testConstructor(self):
		sim = Simulator()
		pos = [0,0,0,0,0]
		ap = Airplane(pos,1, 0, 0, math.pi, math.pi/2); ap.addSimulator(sim)
		uc = UserController(sim,ap)

	# Test after calling the method getControl that a Control object is returned.
	def testGetControl(self):
		c = Control(5,0,20)
		self.assertEqual(type(Control(5,0,20)), c)

if __name__ == '__main__':
	unittest.main()