# LeadingController.py
# Assignment 3

# Author: Alessandro Lira

import math, threading, sys

from Simulator import *
from Airplane import *
from PlaneController import *
from IllegalArgumentException import *

class LeadingController(PlaneController):
	
	def __init__(self,sim,ap):
		# initializes super class
		super(LeadingController, self).__init__(sim,ap)
		
		self.__ap = ap
		self.__apList = []

	# Adds a Airplane to the list of chasers considered by this
    # groundPlane.
	def addFollower(self,ap):
		self.__apList.append(ap)

	# Return a Airplane at index
	def getFollower(self,index):
		if index<0 or index>(len(self.__apList)-1):
			return None
		return self.__apList[index]

	# Returns a control negating the output for the FollowingControler. Added
    # special controls when the Airplane is close to the walls.
	def getControl(self,sec,msec):
		closestAP = self.getClosestPlane()

		# if no closest vehicle return None
		if closestAP is None:
			return None

		desiredOmega = 0

		chaserPos = closestAP.getPosition() # Shared Resource
		myPos = self.__ap.getPosition() # Shared Resource

		# Attempt to get more than one lock - uncomment below to see exception thrown*/
		
		# leadAP = self.__ap
		# print '---Aquiring Multiple AP-Locks---\n'
		# closestAP.ap_lock.acquire()
		# leadAP.ap_lock.acquire()
		# print '---Both AP-Locks Acquired---\n'
		# # The following call to getPosition() will cause DeadLockTester to
		# # throw an exception, since two different ap-locks have been acquired 
		# # by a single thread. The program execution will hault becasue of this
		# closestAP.getPosition()
		# leadAP.getPosition()
		# leadAP.ap_lock.release()
		# closestAP.ap_lock.release()

	    
		xDiff = chaserPos[0] - myPos[0]
		yDiff = chaserPos[1] - myPos[1]
		targetTheta = math.atan2(yDiff, xDiff)

		desiredOmega = PlaneController.normalizeAngle(targetTheta - myPos[2] + math.pi)

		gain = 5.0
		desiredOmega *= gain
		if desiredOmega > math.pi/4:
			desiredOmega = math.pi/4
		if desiredOmega < -math.pi/4:
			desiredOmega = -math.pi/4

		desiredSpeed = 10

		# Wall cases and corner cases
		a = PlaneController.avoidWalls(myPos)
		if a is not None:
			return a

		c = Control(desiredSpeed, desiredOmega)
		return c

	def getClosestPlane(self):

		leaderPos = self.__ap.getPosition()
		closestDist = sys.float_info.max
		closestAP = None
		for ap in self.__apList:
			followerPos = ap.getPosition()
			xDist = leaderPos[0] - followerPos[0]
			yDist = leaderPos[1] - followerPos[1]
			totalDist = math.hypot(xDist, yDist)

			if totalDist < closestDist:
				closestDist = totalDist
				closestAP = ap

		assert (closestAP is not None)
		return closestAP
