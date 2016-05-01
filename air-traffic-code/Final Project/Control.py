# Control.py
# Final Project

# Author: Frederick Daso

import math

from IllegalArgumentException import *

class Control:
	
	def __init__(self,s,omegaX,omegaZ):
		# Check to make sure speed and omegaZ are in range
		if (s<5 or s>10):
			raise IllegalArgumentException("Speed out of range")
		if (omegaZ<-math.pi or omegaZ>=math.pi):
			raise IllegalArgumentException("OmegaZ out of range")
		if (omegaX < -math.pi/2 or omegaX >= math.pi/2)
			raise IllegalArgumentException("OmegaX out of range")

		self.__s = s
		self.__omegaX = omegaX
		self.__omegaZ = omegaZ

	def getSpeed(self):
		return self.__s

	def getRotVelX(self):
		return self.__omegaX
		
	def getRotVelZ(self):
		return self.__omegaZ

