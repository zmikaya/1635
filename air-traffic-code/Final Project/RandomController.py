# RandomController.py
# Assignment 3

# Author: Alessandro Lira

import math, threading, random

from IllegalArgumentException import *
from PlaneController import *
from Airplane import *
from Simulator import *

class RandomController(PlaneController):
	
	def __init__(self,sim,ap):
		# initializes super class
		super(RandomController, self).__init__(sim,ap)

		self.__ap = ap

		self.__minTransSpeed = 5
		self.__maxTransSpeed = 8
		self.__maxRotXSpeed = math.radians(10)
		self.__maxRotZSpeed = math.radians(5)
		self.__controllerInitialized = False
		self.__avoidWallDist = 15

	def getControl(self,sec,msec):
		if type(sec) != float or type(sec) != int:
			raise IllegalArgumentException("Wrong object type")
		if type(msec) != float or type(msec) != int:
			raise IllegalArgumentException("Wrong object type")
		# avoid walls if we're too close
		a = PlaneController.avoidWalls(self.__ap.getPosition())

		if a is not None:
			return a
		# otherwise generate a random control
		randSpeed = random.random()*5 + 5
		randOmegaX = random.random()*math.pi/2.0 - math.pi/4.0
		randOmegaZ = random.random()*math.pi/4.0 - math.pi/8.0
		c = Control(randSpeed,randOmegaX, randOmegaZ)

		return c

