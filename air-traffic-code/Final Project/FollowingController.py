# FollowingController.py
# Assignment 3

# Author: Alessandro Lira

import math, threading

from Simulator import *
from Airplane import *
from PlaneController import *
from IllegalArgumentException import *

class FollowingController(PlaneController):
	
	def __init__(self,sim,followingPlane,targetPlane):
		# initializes super class
		super(FollowingController, self).__init__(sim,followingPlane)

		self.__gv = followingPlane
		self.__leaderAP = targetPlane

	def getControl(self,sec,msec):
		leaderPos = self.__leaderAP.getPosition()
		myPos = self.__gv.getPosition()

		# heading of the leading Plane in global reference

		xDiff = leaderPos[0] - myPos[0]
		yDiff = leaderPos[1] - myPos[1]
		
		if (math.fabs(xDiff) < 1e-6):
			# edge cases for xDiff ~= 0
			if yDiff > 0: 
				desiredTheta = math.pi/2
			else: 
				desiredTheta = -math.pi/2
		else:
			desiredTheta = math.atan2(yDiff,xDiff)

		gain = 5

		# need change in angle
		desiredTheta = PlaneController.normalizeAngle(desiredTheta)
		desiredOmega = PlaneController.normalizeAngle(desiredTheta - myPos[2])

		desiredOmega *= gain

		# bound desired omega
		if desiredOmega > math.pi/4:
			desiredOmega = math.pi/4
		if desiredOmega < -math.pi/4:
			desiredOmega = -math.pi/4

		distance = math.sqrt(xDiff*xDiff + yDiff*yDiff)
		desiredSpeed = distance
		# bound desired speed
		if desiredSpeed > 10:
			desiredSpeed = 10
		if desiredSpeed < 5:
			desiredSpeed = 5

		a = PlaneController.avoidWalls(self.__gv.getPosition())
		if a is not None:
			return a

		newControl = Control(desiredSpeed,desiredOmega)
		return newControl
