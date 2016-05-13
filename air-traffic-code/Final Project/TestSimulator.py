# TestSimulator.py
# Assignment 3

# Author: Alessandro Lira

import unittest

from Simulator import *

class TestSimulator(unittest.TestCase):

	# Constructs a Simulator Object and tests if the constructor __init__ method
	# properly initializes a simulator object with no raised exceptions, and checks
	# to see that currentSec and currentMSec are initialized to = 0
	def testGoodConstructor(self):
		sim = Simulator()
		self.assertTrue(sim.getCurrentSec() == 0)
		self.assertTrue(sim.getCurrentMSec() == 0)

	# Constructs a Simulator Object and tests if the value returned by the
	# function "getCurrentSec()" in the Simulator class is 0 before method
	# "run()" is called
	def testGetSec(self):
		sim = Simulator()
		self.assertAlmostEqual(0, sim.getCurrentSec())

	# Constructs a Simulator Object and tests if the value returned by the
	# function "getCurrentMSec()" in the Simulator class is 0 before method
	# "run()" is called
	def testGetMSec(self):
		sim = Simulator()
		self.assertAlmostEqual(0, sim.getCurrentMSec())

	# Tests if the "advanceClock()" updates the simulator clock increasing it
	# by 100 milliseconds
	def testAdvanceClock(self):
		sim = Simulator()
		sim.advanceClock()

		actualTime = sim.getCurrentSec() + sim.getCurrentMSec()/1e3
		expectedTime = 1e-2
		self.assertAlmostEqual(actualTime, expectedTime)

		# Test if variable sec is increased by 1 and msec = 0 when calling
		# "advanceClock()" 
		sim2 = Simulator()
		for i in range(100):
			sim2.advanceClock()

		self.assertEqual(sim2.getCurrentSec(), 1)
		self.assertEqual(sim2.getCurrentMSec(), 0)

	def testAddVehicle(self):
		sim = Simulator()
		pose = [0,0,0,0,0]
		ap1 = Airplane(pose,1,0,1,0,1, "test")
		ap2 = Airplane(pose,0,1,1,1,0, "test")
		ap1.addSimulator(sim)
		ap2.addSimulator(sim)
		sim.addAirplane(ap1)
		sim.addAirplane(ap2)

		self.assertEqual(ap1,sim._apList[0])
		self.assertEqual(ap2,sim._apList[1])
		
#	def testStreamData(self):
#		sim = Simulator()
		


# main method which executes unit tests when TestSimulator.py is run directly
if __name__ == "__main__":
	unittest.main()