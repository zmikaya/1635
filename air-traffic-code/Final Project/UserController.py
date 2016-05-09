# RandomController.py
# Assignment 3

# Author: Alessandro Lira

import math, threading, random

from IllegalArgumentException import *
from PlaneController import *
from Airplane import *
from Simulator import *

class UserController(PlaneController):
	
	def __init__(self,sim,ap):
		# initializes super class
		super(UserController, self).__init__(sim,ap)

		self.__ap = ap
		self.__sim = sim
		
		self.__minTransSpeed = 5
		self.__maxTransSpeed = 8
		self.__maxRotXSpeed = math.radians(10)
		self.__maxRotZSpeed = math.radians(5)
		self.__controllerInitialized = False
		self.__avoidWallDist = 15
		
	def getThrottle(self):
		aircraft_collection = self.__sim.aircraft_collection
		throttle = aircraft_collection.find_one({'name': 'b2'})['throttle']
		return throttle

	def getControl(self,sec,msec):
		throttle = self.getThrottle()
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

