# Airplane.py
# Assignment 3

# Author: Alessandro Lira

import math, threading, sys, random

from IllegalArgumentException import *
from DeadlockTesterException import *
from DeadlockTester import *

class Airplane(threading.Thread):
	# static class members (call using: Class.<member>)
	totalNumPlanes = 0
	# A simple re-entrant lock suffices here becasue this
	# lock is only used for gated access to the resource
	ap_class_lock = threading.RLock()

	def __init__(self,pos,dx,dy,dz,dtheta, dphi, player_id):
		threading.Thread.__init__(self)

		# check for legal arguments
		if len(pos) != 5:
			raise IllegalArgumentException("Incorrect size Pos array")

		# initiate Airplane
		self.__x = pos[0]
		self.__y = pos[1]
		self.__z = pos[2]
		self.__theta = pos[3]
		self.__phi = pos[4]
		
		self.player_id = player_id

		self.__dx = dx
		self.__dy = dy
		self.__dz = dz
		self.__dtheta = dtheta
		self.__dphi = dphi

		# intrinsic "self" lock
		self.ap_lock = threading.RLock()

		# self.clampPosition()
		# self.clampVelocity()

		self.__sim = None

		self.__lastCheckedSec = 0
		self.__lastCheckedMSec = 0

		# synchronize incrementation on all ap objects
		Airplane.ap_class_lock.acquire()
		self.__planeID = Airplane.totalNumPlanes
		Airplane.totalNumPlanes += 1
		Airplane.ap_class_lock.release()

	def addSimulator(self, sim):
		self.__sim = sim

	def getPlaneID(self):
		return self.__planeID

	# def clampPosition(self): # clamps position values (useful immediately after values have been changed)

	# 	# clamp X&Y&Z values if necessary
	# 	self.__x = min(max(self.__x,0),100)
	# 	self.__y = min(max(self.__y,0),100)
	# 	self.__z = min(max(self.__z,0),100)
		
	# 	# wrap Theta & Phi angle values if necessary
	# 	self.__theta = min(max(self.__theta, -math.pi), math.pi)
	# 	self.__phi = min(max(self.__phi, -math.pi/2), math.pi/2)
	# 	if (math.fabs(self.__theta-math.pi) < 1e-6):
	# 		self.__theta = -math.pi
	# 	if (math.fabs(self.__phi-math.pi/2) < 1e-6):
	# 		self.__phi = -math.pi/2

	# def clampVelocity(self): # clamps velocity values (useful immediately after values have been changed)
		
	# 	speed = math.sqrt(self.__dx*self.__dx + self.__dy*self.__dy + self.__dz*self.__dz)

	# 	# clamp dx & dy values if necessary
	# 	if (speed < 5):
	# 		if speed == 0: speed = 1 # condition to catch div/0 error
	# 		self.__dx = self.__dx*(5/speed)
	# 		self.__dy = self.__dy*(5/speed)
	# 		self.__dz = self.__dz*(5/speed)
	# 	elif (speed > 10):
	# 		self.__dx = self.__dx*(10/speed)
	# 		self.__dy = self.__dy*(10/speed)
	# 		self.__dz = self.__dz*(10/speed)
	

	# 	# clamp dtheta value (rotational velocity) if necessary
	# 	if (self.__dtheta < -math.pi/4):
	# 		self.__dtheta = -math.pi/4
	# 	elif (self.__dtheta > math.pi/4):
	# 		self.__dtheta = math.pi/4
		
	# 	# clamp dphi value (rotational velocity) if necessary
	# 	if (self.__dphi < -math.pi/8):
	# 		self.__dphi = math.pi/8
	# 	elif (self.__dphi > math.pi/8):
	# 		self.__dphi = math.pi/8

	# 	self.__dtheta = min(max(self.__dtheta,-math.pi/4),math.pi/4)
	# 	self.__dphi = min(max(self.__dphi, -math.pi/8), math.pi/8)

	def checkIfNoLock(self):
		if self.__sim is None:
			return False
		try:
			return DeadlockTester.testLock(self,self.__sim)
		except DeadlockTesterException, e:
			print e
			sys.exit()

		return False

	def getPosition(self):
		pos = []
		if self.checkIfNoLock():
			self.ap_lock.acquire() # start critical region
			pos = [self.__x, self.__y,self.__z, self.__theta, self.__phi]
			self.ap_lock.release() # end critical region
			return pos

		return pos

	def getVelocity(self):
		vel = []
		if self.checkIfNoLock():
			self.ap_lock.acquire() # start critical region
			vel = [self.__dx, self.__dy, self.__dz, self.__dtheta, self.__dphi]
			self.ap_lock.release() # end critical region
			return vel

		return vel

	def setPosition(self,pos):
		if len(pos) != 5:
			raise IllegalArgumentException("new Pos array must be of length 3")

		self.ap_lock.acquire() # start critical region
		self.__x = pos[0]
		self.__y = pos[1]
		self.__z = pos[2]
		self.__theta = pos[3]
		self.__phi = pos[4]

		# self.clampPosition()
		self.ap_lock.release() # end critical region

	def setVelocity(self,vel):
		if len(vel) != 5:
			raise IllegalArgumentException("new Vel array must be of length 3")

		self.ap_lock.acquire() # start critical region
		self.__dx = vel[0]
		self.__dy = vel[1]
		self.__dz = vel[2]
		self.__dtheta = vel[3]
		self.__dphi = vel[4]

		# self.clampVelocity()
		self.ap_lock.release() # end critical region

	def controlPlane(self,c):
		speed = c.getSpeed()
		dtheta = c.getRotVelZ()
		dphi = c.getRotVelX()

		self.ap_lock.acquire() # start critical region
		# modify internal dx and dy values
		self.__dx = speed*math.cos(self.__theta)
		self.__dy = speed*math.sin(self.__theta)
		self.__dz = speed*math.sin(self.__phi)

		# change dtheta and dphi to supplied rotational velocities
		self.__theta = dtheta
		self.__phi = dphi
		# self.clampVelocity()
		self.ap_lock.release() # end critical region

	@staticmethod
	def normalizeAngleTheta(theta):

		rtheta = math.fmod(theta - math.pi, 2*math.pi)
		if rtheta < 0:
			rtheta += 2*math.pi

		rtheta -= math.pi

		return rtheta
		
	@staticmethod	
	def normalizeAnglePhi(phi):
		
		rphi = math.fmod(phi - math.pi/2, math.pi)
		if rphi < 0:
			rphi += math.pi
			
		rphi -= math.pi/2
		
		return phi

	def advance(self,sec,msec):
		t = sec + msec*1e-3;

		self.ap_lock.acquire() # start critical region

		noiseScaleFactor = 200 # adjust to determine noise magnitude

		errc = random.gauss(0,10)/noiseScaleFactor
		errd = random.gauss(0,20)/noiseScaleFactor

		self.__x = self.__x + self.__dx*t + errd*math.cos(self.__theta) - errc*math.sin(self.__theta)
		self.__y  = self.__y + self.__dy*t + errd*math.sin(self.__theta) + errc*math.cos(self.__theta)
		self.__z = self.__z + self.__dz*t + errc*math.cos(self.__phi) + errd*math.sin(self.__phi)
		self.__theta = self.normalizeAngleTheta(self.__theta + self.__dtheta*t)
		self.__phi = self.normalizeAnglePhi(self.__phi + self.__dphi*t)

		s = math.sqrt(self.__dx*self.__dx + self.__dy*self.__dy + self.__dz*self.__dz)
		self.__dx = s*math.cos(self.__theta)
		self.__dy = s*math.sin(self.__theta)
		self.__dz = s*math.cos(self.__phi)
		self.__dtheta = self.__dtheta
		self.__dphi = self.__dphi

		self.clampPosition()
		self.clampVelocity()

		self.ap_lock.release() # end critical region
		
	def advanceNoiseFree(self,sec,msec):
		t = sec + msec*1e-3;

		# -- Linear approximation --
		#	see previous solution for linear approximation model

		# -- Curve model --
		
		self.ap_lock.acquire() # start critical region

		# Assuming that  dx,  dy, and  dtheta was set beforehand by controlPlane()
		s = math.sqrt(self.__dx*self.__dx + self.__dy*self.__dy + self.__dz*self.__dz)
		
		if (abs(self.__dtheta) > 1e-3): # The following model is not well defined when dtheta = 0
			# Circle center and radius
			r = s/self.__dtheta
			# print 'theta: {0}; phi {1}'.format(self.__theta, self.__phi)
			xc = self.__x - r * math.sin(self.__theta)
			yc = self.__y + r * math.cos(self.__theta)
			zc = self.__z + r * math.sin(self.__phi)

			self.__theta = self.__theta + self.__dtheta*t

			rtheta = ((self.__theta-math.pi) % (2*math.pi))
			rphi = ((self.__phi - math.pi/2) % (math.pi))
			if (rtheta < 0): # Note that % in java is remainder, not modulo.
				rtheta += 2*math.pi
			if (rphi < 0):
				rphi += math.pi

			self.__theta = rtheta - math.pi;
			self.__phi = rphi - math.pi;

			# Update Values
			self.__x = xc + r * math.sin(self.__theta)
			self.__y = yc - r * math.cos(self.__theta)
			self.__z = zc - r * math.cos(self.__phi)
			self.__dx = s * math.cos(self.__theta)
			self.__dy = s * math.sin(self.__theta)
			self.__dz = s * math.sin(self.__phi)
			# print self.__dy
			# self.__x = self.__x + self.__dx*t
			# self.__y = self.__y + self.__dy*t
			# self.__z = self.__z + self.__dz*t
			
		else:	# Straight motion. No change in theta.
			# print self.__dy
			print 'theta: {0}; phi {1}'.format(self.__theta, self.__phi)
			self.__dx = s * math.cos(self.__theta)
			self.__dy = s * math.sin(self.__theta)
			self.__dz = s * math.sin(self.__phi)
			self.__x = self.__x + self.__dx*t
			self.__y = self.__y + self.__dy*t
			self.__z = self.__z + self.__dz*t
			
		# self.clampPosition()
		# self.clampVelocity()

		self.ap_lock.release() # end critical region

	def run(self):

		print "ap: %i thread started" % self.__planeID

		currentSec = 0
		currentMSec = 0

		while (currentSec < self.__sim.duration) and not self.__sim.halt:
		# 	if not self.__sim.getDisplayClient().isConnected():
		# 		break

			# Start Condition Critical Region
			self.__sim.simulator_lock.acquire()

			currentSec = self.__sim.getCurrentSec()
			currentMSec = self.__sim.getCurrentMSec()

			while 1:

				# check if time has changed since last update
				if not (self.__lastCheckedSec == currentSec and 
						self.__lastCheckedMSec == currentMSec):

					currentSec = self.__sim.getCurrentSec()
					currentMSec = self.__sim.getCurrentMSec()
					break # exit "while 1" loop once current time is updated

				# wait until Simulator notifies all threads that time has passed
				self.__sim.simulator_lock.wait() 
												 
				currentSec = self.__sim.getCurrentSec()
				currentMSec = self.__sim.getCurrentMSec()

			self.advanceNoiseFree(0,10)
			#self.advance(0,10)

			# End Condition Critical Region
			self.__sim.simulator_lock.release()

			# update the time of the last control
			self.__lastCheckedSec = currentSec
			self.__lastCheckedMSec = currentMSec

			# start critical region
			self.__sim.simulator_lock.acquire()

			# decrement number of controllers left to update
			if self.__sim.numPlaneToUpdate > 0:
				self.__sim.numPlaneToUpdate -= 1
			self.__sim.simulator_lock.notify_all()

			# end critical region
			self.__sim.simulator_lock.release() 


	# The following three methods (getPlaneLock, compareId,
	# reverseCompareId) is is needed when you try resource-hierarchy
	# solution for deadlock prevention

	# def compareID(self,ap):
	# 	if self.getPlaneID < ap.getPlaneID:
	# 		return -1
	# 	elif self.getPlaneID < ap.getPlaneID:
	# 		return 1
	# 	else:
	# 		return 0

	# def reverseCompareID(self,ap):
	# 	return -(self.compareID(ap))


