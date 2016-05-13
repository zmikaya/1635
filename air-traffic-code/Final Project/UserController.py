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
		player_id = self.__sim.player_id
		throttle = aircraft_collection.find_one({'_id': player_id})['throttle']
		return throttle
		
	def getPitch(self):
		aircraft_collection = self.__sim.aircraft_collection
		player_id = self.__sim.player_id
		pitch = aircraft_collection.find_one({'_id': player_id})['pitch']
		return -pitch
		
	def getRoll(self):
		aircraft_collection = self.__sim.aircraft_collection
		player_id = self.__sim.player_id
		roll = aircraft_collection.find_one({'_id': player_id})['roll']
		return -roll

	def getControl(self,sec,msec):
		throttle = self.getThrottle()
		pitch = self.getPitch()
		roll = self.getRoll()
		# print pitch
		# avoid walls if we're too close
		# a = PlaneController.avoidWalls(self.__ap.getPosition())

		# if a is not None:
		# 	return a
		# otherwise generate a random control
		speed = throttle*15
		omegaX = roll
		omegaZ = pitch
		c = Control(speed, omegaX, omegaZ)

		return c

