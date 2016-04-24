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

		self.__ap = followingPlane
		self.__leaderAP = targetPlane

	def getControl(self,sec,msec):
		leaderPos = self.__leaderAP.getPosition()
		myPos = self.__ap.getPosition()

		# heading of the leading Plane in global reference

		xDiff = leaderPos[0] - myPos[0]
		yDiff = leaderPos[1] - myPos[1]
		zDiff = leaderPos[2] - myPos[2]
		
		if (math.fabs(xDiff) < 1e-6):
			# edge cases for xDiff ~= 0
			if yDiff > 0: 
				desiredTheta = math.pi/2
			else: 
				desiredTheta = -math.pi/2
		else:
			desiredTheta = math.atan2(yDiff,xDiff)
			
		if (math.fbs(zDiff) < 1e-6):
			# edge cases for zDiff ~= 0
			if yDiff > 0:
				desiredPhi = math.pi/4
			else:
				desiredPhi = -math.pi/4
		else:
			desiredPhi = math.atan2(zDiff,yDiff)

		gain = 5

		# need change in angle
		desiredTheta = PlaneController.normalizeAngleTheta(desiredTheta)
		desiredOmegaX = PlaneController.normalizeAngleTheta(desiredTheta - myPos[3])
		
		desiredPhi = PlaneController.normalizeAnglePhi(desiredPhi)
		desiredOmegaZ = PlaneController.normalizeAnglePhi(desiredPhi - myPos[4])

		desiredOmegaX *= gain
		desiredOmegaZ *= 0.5*gain

		# bound desired omega
		if desiredOmegaX > math.pi/4:
			desiredOmegaX = math.pi/4
		if desiredOmegaX < -math.pi/4:
			desiredOmegaX = -math.pi/4
			
		# bound desired phi
		if desiredOmegaZ > math.pi/8:
			desiredOmegaZ > math.pi/8
		if desiredOmegaZ > -math.pi/8:
			desiredOmegaZ = -math.pi/8

		distance = math.sqrt(xDiff*xDiff + yDiff*yDiff + zDiff*zDiff)
		desiredSpeed = distance
		# bound desired speed
		if desiredSpeed > 10:
			desiredSpeed = 10
		if desiredSpeed < 5:
			desiredSpeed = 5

		a = PlaneController.avoidWalls(self.__ap.getPosition())
		if a is not None:
			return a

		newControl = Control(desiredSpeed,desiredOmegaX, desiredOmegaZ)
		return newControl
