# TestLeadingController.py
# Assignment 3

# Author: Alessandro Lira

import unittest, math

from IllegalArgumentException import *
from FollowingController import *
from PlaneController import *
from LeadingController import *
from Airplane import *
from Simulator import *
from Control import *

class TestLeadingController(unittest.TestCase):

	# Test constructor does not throw an error
	def testConstructor(self):
		sim = Simulator()
		pos = [0,0,0]
		ap = Airplane(pos,1,0,math.pi); ap.addSimulator(sim)
		pc = PlaneController(sim,ap)

	# Tests that following vehicles are correctly added to the 
	# Leading Controller
	def testAddFollower(self):
		sim = Simulator()

		pos = [1,2,3]

		ap1 = Airplane(pos,0,0,0); ap1.addSimulator(sim)
		ap2 = Airplane(pos,1,1,1); ap2.addSimulator(sim)

		lc = LeadingController(sim, ap1)
		lc.addFollower(ap2)

		self.assertEqual(ap2, lc.getFollower(0))

	def testGetClosestPlane(self):
		sim = Simulator()

		pos1 = [50,50,0]
		pos2 = [10,10,0]
		pos3 = [100,100,0]

		ap1 = Airplane(pos1,5,0,0); ap1.addSimulator(sim)
		ap2 = Airplane(pos2,0,5,0); ap2.addSimulator(sim)
		ap3 = Airplane(pos3,10,0,0); ap3.addSimulator(sim)


		lc = LeadingController(sim, ap1)
		lc.addFollower(ap2)
		lc.addFollower(ap3)

		self.assertEqual(ap2, lc.getClosestPlane())

if __name__ == '__main__':
	unittest.main()