# TestControl.py
# Assignment 3

# Author: Alessandro Lira

import unittest

from IllegalArgumentException import *
from Control import *

class TestControl(unittest.TestCase):

	# test illegal arguments
	def testLowS(self):
		with self.assertRaises(IllegalArgumentException):
			c = Control(-4,0,0)	
	
	def testHighS(self):
		with self.assertRaises(IllegalArgumentException):
			c = Control(1100,0,0)
	
	def testLowOmegaX(self):
		with self.assertRaises(IllegalArgumentException):
			c = Control(5,-10,0)

	def testHighOmegaX(self):
		with self.assertRaises(IllegalArgumentException):
			c = Control(5,10,0)
	
	def testLowOmegaZ(self):
		with self.assertRaises(IllegalArgumentException):
			c = Control(5,0,-10)

	def testHighOmegaZ(self):
		with self.assertRaises(IllegalArgumentException):
			c = Control(5,0,10)

	# test legal arguments
	def testCorrectOutputs(self):
		# values which should not throw errors
		test_s = 7.5
		test_omegaX = .2
		test_omegaZ = .1
		test_c = Control(test_s,test_omegaX, test_omegaZ)
		
		self.assertEqual(test_s, test_c.getSpeed())
		self.assertEqual(test_omegaX, test_c.getRotVelX())
		self.assertEqual(test_omegaZ, test_c.getRotVelZ())


# main method which executes unit tests when TestControl.py is run directly
if __name__ == "__main__":
	unittest.main()


