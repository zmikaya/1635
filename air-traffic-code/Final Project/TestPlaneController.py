# TestPlaneController.py
# Assignment 3

# Author: Alessandro Lira

import unittest, math

from IllegalArgumentException import *
from FollowingController import *
from PlaneController import *
from Airplane import *
from Simulator import *
from Control import *

class TestPlaneController(unittest.TestCase):

	# Test constructor does not throw an error
	def testConstructor(self):
		sim = Simulator()
		pos = [0,0,0]
		ap = Airplane(pos,1,0,math.pi); ap.addSimulator(sim)
		pc = PlaneController(sim,ap)

	# Tests if after calling the method "setNumSides (int n)" the variable
    # "sides" gets correctly updated.
	def testSetSides(self):
		sim = Simulator()
		pose = [0,0,0]
		ap = Airplane(pose,1,0,math.pi)
		pc = PlaneController(sim,ap)

		# values within boundaries
		self.assertEqual(7,pc.setNumSides(7))
		self.assertEqual(4,pc.setNumSides(4))

		# above upper boundry, value does not change
		self.assertEqual(4,pc.setNumSides(25))
		#below lower boundart, value still doesn't change
		self.assertEqual(4,pc.setNumSides(2))

if __name__ == '__main__':
	unittest.main()
