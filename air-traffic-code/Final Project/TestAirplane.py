# TestAirplane
# Assignment 3

# Author: Alessandro Lira

import unittest, math

from IllegalArgumentException import *
from Airplane import *
from Simulator import *
from Control import *

class TestAirplane(unittest.TestCase):

	# Contructs valid AP to ensusre that no exceptions are thrown;
	# also confirms that the AP arguments are properly set
	def testConstructor(self):
		pose = [1,2,0,0,0]
		dx = 5
		dy = 0
		dz = 0
		dtheta = 0
		dphi = 0
		ap = Airplane(pose, dx, dy, dz, dtheta, dphi, 'dummy')
		sim = Simulator()
		ap.addSimulator(sim)
		
		# Note: self.assertAlmostEqual() compares two arguments up
		#       to 7 decimal places by default. This amount can be 
		#       modified by including a third argument

		newPose = ap.getPosition()
		self.assertAlmostEqual(pose[0], newPose[0])
		self.assertAlmostEqual(pose[1], newPose[1])
		self.assertAlmostEqual(pose[2], newPose[2])
		self.assertAlmostEqual(pose[3], newPose[3])
		self.assertAlmostEqual(pose[4], newPose[4])

		newVel = ap.getVelocity()
		self.assertAlmostEqual(dx, newVel[0])
		self.assertAlmostEqual(dy, newVel[1])
		self.assertAlmostEqual(dz, newVel[2])
		self.assertAlmostEqual(dtheta, newVel[3])
		self.assertAlmostEqual(dphi, newVel[4])

	def testTooManyArgumentsConstructor(self):
		with self.assertRaises(IllegalArgumentException):
			pose = [0,0,0,0,0,0]
			ap = Airplane(pose, 0, 0, 0, 0, 0, "dummy")

	def testTooFewArgumentsConstructor(self):
		with self.assertRaises(IllegalArgumentException):
			pose = [0,0]
			ap = Airplane(pose, 0, 0, 0, 0, 0, "dummy")

	def testNonArrayPoseArgument(self):
		with self.assertRaises(IllegalArgumentException):
			pose = 'not an array'
			ap = Airplane(pose, 0, 0, 0, 0, 0, "dummy")

	def testTooManyArgumentsSetPosition(self):
		with self.assertRaises(IllegalArgumentException):
			ap = Airplane([0,0,0,0,0], 5, 0, 0,0,0, "test")
			ap.setPosition([0,0,0,0,0,0,0])

	def testTooFewArgumentsSetPosition(self):
		with self.assertRaises(IllegalArgumentException):
			ap = Airplane([0,0,0,0,0], 5, 0, 0,0,0, "test")
			ap.setPosition([0,0])

	def testTooManyArgumentsSetVelocity(self):
		with self.assertRaises(IllegalArgumentException):
			ap = Airplane([0,0,0,0,0], 5, 0, 0, 0, 0, "test")
			ap.setVelocity([0,0,0,0,0,0,0])

	def testTooFewArgumentsSetVelocity(self):
		with self.assertRaises(IllegalArgumentException):
			ap = Airplane([0,0,0,0,0], 5, 0, 0, 0 ,0, "test")
			ap.setVelocity([0,0])

	# Test get/set Position/Velocity at all legal position bounds
	def testGetSetPosVelValid(self):
		pose = [1,2,0,0,0]
		dx = 5
		dy = 0
		dz = 0
		dtheta = 0
		dphi = 0
		ap = Airplane(pose, dx, dy, dz, dtheta, dphi, "test")
		sim = Simulator()
		ap.addSimulator(sim)		
		
		# test get pos/vel values match inputs of constructor
		newPose = ap.getPosition()
		self.assertAlmostEqual(pose[0], newPose[0])
		self.assertAlmostEqual(pose[1], newPose[1])
		self.assertAlmostEqual(pose[2], newPose[2])

		newVel = ap.getVelocity()
		self.assertAlmostEqual(dx, newVel[0])
		self.assertAlmostEqual(dy, newVel[1])
		self.assertAlmostEqual(dz, newVel[2])

		# First, test getPosition and setPostion at legal bounds
		
		# x-position near-boundary conditions
		pose[0] = 0
		ap.setPosition(pose)
		newPose = ap.getPosition()
		self.assertAlmostEqual(pose[0], newPose[0])

		pose[0] = 99
		ap.setPosition(pose)
		newPose = ap.getPosition()
		self.assertAlmostEqual(pose[0], newPose[0])

		# y-position near-boundary conditions
		pose[1] = 0
		ap.setPosition(pose)
		newPose = ap.getPosition()
		self.assertAlmostEqual(pose[1], newPose[1])

		pose[1] = 99
		ap.setPosition(pose)
		newPose = ap.getPosition()
		self.assertAlmostEqual(pose[1], newPose[1])

		# theta near-boundary conditions
		pose[3] = -math.pi
		ap.setPosition(pose)
		newPose = ap.getPosition()
		self.assertAlmostEqual(pose[2], newPose[2])

		pose[3] = math.radians(179)
		ap.setPosition(pose)
		newPose = ap.getPosition()
		self.assertAlmostEqual(pose[2], newPose[2])

		# Test getVelocity and setVelocity at all legal position bounds
		vel = ap.getVelocity()

		# x-velocity near-boundary conditions
		vel[0] = 5
		vel[1] = 0
		ap.setVelocity(vel)
		newVel = ap.getVelocity()
		self.assertAlmostEqual(vel[0], newVel[0])

		vel[0] = 10
		vel[1] = 0
		ap.setVelocity(vel)
		newVel = ap.getVelocity()
		self.assertAlmostEqual(vel[0], newVel[0])

		# y-velocity near-boundary conditions
		vel[0] = 0
		vel[1] = 5
		ap.setVelocity(vel)
		newVel = ap.getVelocity()
		self.assertAlmostEqual(vel[1], newVel[1])

		vel[0] = 0
		vel[1] = 10
		ap.setVelocity(vel)
		newVel = ap.getVelocity()
		self.assertAlmostEqual(vel[1], newVel[1])	

		# omega near-boundary conditions
		vel[2] = -math.pi/4
		ap.setVelocity(vel)
		newVel = ap.getVelocity()
		self.assertAlmostEqual(vel[2], newVel[2])	

		vel[2] = math.pi/4
		ap.setVelocity(vel)
		newVel = ap.getVelocity()
		self.assertAlmostEqual(vel[2], newVel[2])	

	def testGetSetPosVelInvalid(self):
		pose = [1,2,0,0,0]
		dx = 5
		dy = 0
		dz = 0
		dtheta = 0
		dphi = 0
		ap = Airplane(pose, dx, dy, dz, dtheta, dphi, "test")
		sim = Simulator()
		ap.addSimulator(sim)

		# Test getPosition and setPosition at illegal bounds. Since all bounds
		# violations get clamped to legal limits, we can test all three
		# dimensions of position at once. 

		# lower bounds
		pose[0] = -1
		pose[1] = -1
		pose[2] = -1
		pose[3] = -2*math.pi
		pose[4] = -math.pi
		ap.setPosition(pose)
		newPose = ap.getPosition()
		self.assertAlmostEqual(-1, newPose[0])
		self.assertAlmostEqual(-1, newPose[1])
		self.assertAlmostEqual(-1, newPose[2])

		# upper bounds
		pose[0] = 101
		pose[1] = 101
		pose[2] = 101
		pose[3] = 2*math.pi
		pose[4] = math.pi
		ap.setPosition(pose)
		newPose = ap.getPosition()
		self.assertAlmostEqual(101, newPose[0])
		self.assertAlmostEqual(101, newPose[1])
		self.assertAlmostEqual(101, newPose[2])

		# Test getVelocity and setVelocity at illegal bounds. Since all bounds
		# violations get clamped to legal limits, we can test all three
		# dimensions of velocity at once.

		vel = ap.getVelocity()

		# lower bounds
		vel[0] = 0
		vel[1] = 1
		vel[2] = 1
		vel[3] = -math.pi
		vel[4] = -3
		ap.setVelocity(vel)
		newVel = ap.getVelocity()
		self.assertAlmostEqual(0, newVel[0])
		self.assertAlmostEqual(1, newVel[1])
		self.assertAlmostEqual(1, newVel[2])

		# upper bounds
		vel[0] = 0
		vel[1] = 20
		vel[2] = 0
		vel[3] = math.pi
		vel[4] = 2*math.pi
		ap.setVelocity(vel)
		newVel = ap.getVelocity()
		self.assertAlmostEqual(0, newVel[0])
		self.assertAlmostEqual(20, newVel[1])
		self.assertAlmostEqual(0, newVel[2])

	# controlVehicle and advanceNoiseFree are tricky to test. You 
	# have to use your judgement as to how to test these. Typically 
	# what happens is that as you develop, you discover edge cases 
	# that need to be added. 

	def testControlVehicle(self):
		pose = [1,2,0,0,0]
		dx = 5
		dy = 0
		dz = 0
		dtheta = 0
		dphi = 0
		ap = Airplane(pose, dx, dy, dz, dtheta, dphi, "test")
		sim = Simulator()
		ap.addSimulator(sim)

		# Acceleration in x

		c = Control(10,0,0)
		ap.controlPlane(c)

		newVel = ap.getVelocity()
		self.assertAlmostEqual(10, newVel[0])
		self.assertAlmostEqual(0, newVel[1])
		self.assertAlmostEqual(0, newVel[2])
		self.assertAlmostEqual(0, newVel[3])
		self.assertAlmostEqual(0, newVel[4])

		# Acceleration in y

		pose = [0,0,0, math.pi/2 ,0]
		ap.setPosition(pose)
		vel = [0,10,0,0,0]
		ap.setVelocity(vel)

		c = Control(10,0,0)
		ap.controlPlane(c)
		
		newVel = ap.getVelocity()
		self.assertAlmostEqual(0, newVel[0])
		self.assertAlmostEqual(10, newVel[1])
		self.assertAlmostEqual(0, newVel[2])
		self.assertAlmostEqual(0, newVel[3])
		self.assertAlmostEqual(0, newVel[4])

		# Acceleration at PI/4 from 5m/s to 10 m/s

		vel[0] = math.sqrt(12.5)
		vel[1] = math.sqrt(12.5)
		vel[2] = 0
		vel[3] = math.pi/4
		vel[4] = 0
		ap.setVelocity(vel)
		c = Control(10,0,0)
		ap.controlPlane(c)

		newVel = ap.getVelocity()
		self.assertAlmostEqual(10, math.sqrt(newVel[0]*newVel[0] + newVel[1]*newVel[1]))

		# Rotational acceleration

		vel[3] = math.pi/4
		ap.setVelocity(vel)
		c = Control(5, math.pi/4, 0)
		ap.controlPlane(c)

		newVel = ap.getVelocity()
		self.assertAlmostEqual(math.pi/4, newVel[3])

	def testAdvanceNoiseFree(self):
		pose = [1,2,0,0,0]
		dx = 5
		dy = 0
		dz = 0
		dtheta = 0
		dphi = 0
		sim = Simulator()
		ap = Airplane(pose, dx, dy, dz, dtheta, dphi, "test")
		ap.addSimulator(sim)

		# Straight-line motion along x
		
		ap.advanceNoiseFree(1, 0)

		newPose = ap.getPosition()
		self.assertAlmostEqual(6,newPose[0])
		self.assertAlmostEqual(2,newPose[1])
		self.assertAlmostEqual(0,newPose[2])

		# Straight-line motion along y
		
		pose = [0,0,0,math.pi/2,0]
		ap.setPosition(pose)
		vel = [0,5,0,0,0]
		ap.setVelocity(vel)

		ap.advanceNoiseFree(1, 0)

		newPose = ap.getPosition()
		print newPose[0]
		self.assertAlmostEqual(0,newPose[0])
		self.assertAlmostEqual(5,newPose[1])
		self.assertAlmostEqual(0,newPose[2])

		# Straight-line motion along PI/4

		pose = [0,0,0,math.pi/4,0]
		ap.setPosition(pose)

		# Set vehicle moving at 5 m/s along PI/4

		vel[0] = math.sqrt(12.5)
		vel[1] = math.sqrt(12.5)
		vel[2] = 0
		ap.setVelocity(vel)

		newVel = ap.getVelocity()
		self.assertAlmostEqual(vel[0], newVel[0])
		self.assertAlmostEqual(vel[1], newVel[1])
		self.assertAlmostEqual(vel[2], newVel[2])

		ap.advanceNoiseFree(1, 0)

		newPose = ap.getPosition()
		self.assertAlmostEqual(math.sqrt(12.5), newPose[0])
		self.assertAlmostEqual(math.sqrt(12.5), newPose[1])
		self.assertAlmostEqual(0, newPose[2])

		# Rotational Motion

		pose = [0,0,0,math.pi/8,0]
		ap.setPosition(pose)

		vel[0] = math.sqrt(5)
		vel[1] = math.sqrt(5)
		vel[2] = 0

		ap.setVelocity(vel)

		ap.advanceNoiseFree(1,0)

		newPose = ap.getPosition()
		self.assertAlmostEqual(math.pi/8, newPose[3])

	# Because advance() has noise, we need to adjust the margin of error 
	# allowed in the assert statements 

	def testAdvance(self):
		pose = [0,2,0,0,0]
		dx = 5
		dy = 0
		dz = 0
		dtheta = 0
		dphi = 0
		sim = Simulator()
		ap = Airplane(pose, dx, dy, dz, dtheta, dphi, "test")
		ap.addSimulator(sim)

		# Straight-line motion along x
		
		ap.advance(1, 0)

		newPose = ap.getPosition()
		self.assertTrue(math.fabs(5 - newPose[0]) < 0.5)
		self.assertTrue(math.fabs(2 - newPose[1]) < 0.5)
		self.assertTrue(math.fabs(0 - newPose[2]) < 0.5)

		# Straight-line motion along y
		
		pose = [0,0,0,0,0]
		ap.setPosition(pose)
		vel = [0,5,0,0,0]
		ap.setVelocity(vel)

		ap.advance(1, 0)

		newPose = ap.getPosition()
		self.assertTrue(math.fabs(0 - newPose[0]) < 0.5)
		self.assertTrue(math.fabs(5 - newPose[1]) < 0.5)
		self.assertTrue(math.fabs(0 - newPose[2]) < 0.5)

		# Straight-line motion along PI/4

		pose = [0,0,0,0,0]
		ap.setPosition(pose)

		# Set vehicle moving at 5 m/s along PI/4

		vel[0] = math.sqrt(12.5)
		vel[1] = math.sqrt(12.5)
		vel[2] = 0
		vel[3] = 0
		vel[4] = 0
		ap.setVelocity(vel)

		newVel = ap.getVelocity()
		self.assertTrue(math.fabs(vel[0] - newVel[0]) < 0.5)
		self.assertTrue(math.fabs(vel[1] - newVel[1]) < 0.5)
		self.assertTrue(math.fabs(vel[2] - newVel[2]) < 0.5)

		ap.advance(1, 0)

		newPose = ap.getPosition()
		self.assertTrue(math.fabs(math.sqrt(12.5) - newPose[0]) < 0.5)
		self.assertTrue(math.fabs(math.sqrt(12.5) - newPose[1]) < 0.5)
		self.assertTrue(math.fabs(0 - newPose[2]) < 0.5)

		# Rotational Motion

		pose = [0,0,0,0,0]
		ap.setPosition(pose)

		vel[0] = math.sqrt(5)
		vel[1] = math.sqrt(5)
		vel[2] = 0
		vel[3] = math.pi/8
		vel[4] = 0

		ap.setVelocity(vel)

		ap.advance(1,0)

		newPose = ap.getPosition()
		self.assertTrue(math.fabs(math.pi/8 - newPose[2]) < 0.5)

	# Tests if the returned angle is in the range [-Pi, Pi)

	# def testNormalizeAngle(self):
	# 	# Within range boundaries
	# 	self.assertAlmostEqual(0, Airplane.normalizeAngle(0))

	# 	# Near upper boundary
	# 	self.assertAlmostEqual(math.radians(179), Airplane.normalizeAngle(math.radians(179)))

	# 	# Near lower boundary
	# 	self.assertAlmostEqual(-math.pi, Airplane.normalizeAngle(-math.pi))

	# 	# Above upper boundary
	# 	self.assertAlmostEqual(-math.pi/2, Airplane.normalizeAngle(3.5*math.pi))

	# 	# Below lower boundary
	# 	self.assertAlmostEqual(math.pi/2, Airplane.normalizeAngle(-3.5*math.pi))




# main method which executes unit tests when TestAirplane.py is run directly
if __name__ == "__main__":
	unittest.main()