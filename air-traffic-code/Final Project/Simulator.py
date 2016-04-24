# Simulator.py
# Assignment 3

# Author: Alessandro Lira

import math, sys, threading, time, random

from IllegalArgumentException import *
from FollowingController import *
from VehicleController import *
from LeadingController import *
from RandomController import *
from GroundVehicle import *
from DisplayClient import *
from Control import *

class Simulator(threading.Thread):

	def __init__(self, displayClient=None):
		threading.Thread.__init__(self)

		self.__currentSec = 0
		self.__currentMSec = 0

		# NOTE: the '_' prefix is python convention, and does not 
		# affect the behavior of the targeted member 
		# (in this case, '_gvList' will behave identically to 'gvList')
		self._gvList = [] # 'protected' class member

		if displayClient is None:
			# print 'WARNING: No DisplayClient specified'
			pass
		self.__displayClient = displayClient
				
		# Non-Private class members
		self.numControlToUpdate = 0
		self.numVehicleToUpdate = 0

		# Public simulator lock
		self.simulator_lock = threading.Condition()

	#[PLACEHOLDER] check if necessary
	# UPDATE: used for quit condition loop
	def getDisplayClient(self):
		return self.__displayClient

	def getCurrentSec(self):
		self.simulator_lock.acquire() # start critical region
		cSec = self.__currentSec
		self.simulator_lock.release() # end critical region
		return cSec

	def getCurrentMSec(self):
		self.simulator_lock.acquire() # start critical region
		cMSec = self.__currentMSec
		self.simulator_lock.release() # end critical region
		return cMSec

	def advanceClock(self):
		self.simulator_lock.acquire() # start critical region
		self.__currentMSec += 10
		if (self.__currentMSec >= 1e3):
			self.__currentMSec -= 1e3
			self.__currentSec += 1
		self.simulator_lock.release() # end critical region

	def addGroundVehicle(self, gv):
		self.simulator_lock.acquire() # start critical region
		self._gvList.append(gv)
		print "---------Adding Ground Vehicle-----------\n"
		i = 1
		for gv in self._gvList:
			pos = gv.getPosition()
			print "%i : %f,%f,%f" %  (i,pos[0],pos[1],pos[2])
			i+=1
		print " "

		self.numControlToUpdate += 1
		self.numVehicleToUpdate += 1
		self.simulator_lock.release() # end critical region

	def run(self):

		# We're going to need these to know how much time has elapsed since the
		# last call to vehicle.updateState(). We could leave this out, and always
		# call vehicle.updateState() with arguments of 0 and 10, but for a
		# real-time implementation in a later assignment, we're actually going to
		# need to measure the elapsed time. 

		lastUpdateSec = self.__currentSec
		lastUpdateMSec = self.__currentMSec

		if self.__displayClient:
			self.__displayClient.clear()
			self.__displayClient.traceOn()

		print "Simulator thread started"

		while (self.__currentSec < 100):
			#[NOT NECESSARY] Implemented for convenience of having the VC and 
			# Sim threads ends when quit is called on the DisplayServer
			if not self.__displayClient.isConnected():
				print 'SIM: display client NOT connected'
				break

			deltaSec = self.__currentSec - lastUpdateSec
			deltaMSec = self.__currentMSec - lastUpdateMSec

			if (deltaMSec < 0):
				deltaMSec += 1e3
				deltaSec -= 1

			gvX = []
			gvY = []
			gvTheta = []

			# populate data to be sent to display client 
			for currentGV in self._gvList:
				pos = currentGV.getPosition()
				vel = currentGV.getVelocity()
				gvX.append(pos[0])
				gvY.append(pos[1])
				gvTheta.append(pos[2])

			# send GV positions to the DisplayServer using the DisplayClient
			if self.__displayClient:
				self.__displayClient.update(len(self._gvList),gvX,gvY,gvTheta)

			# Start of Conditional Critical Region
			self.simulator_lock.acquire() 

			# update the clock
			lastUpdateSec = self.__currentSec
			lastUpdateMSec = self.__currentMSec

			self.advanceClock()
			
			# Notify-All waiting VC threads
			self.simulator_lock.notify_all()

			# End of Conditinal Critical Region
			self.simulator_lock.release()

			# acquire lock to wait for all VCs to finish updating
			self.simulator_lock.acquire() # Start of Conditional Critical Region
			while 1:
				# check if all controllers and vehicles updated, otherwise wait
				if self.numControlToUpdate == 0 and self.numVehicleToUpdate == 0:
					break
				self.simulator_lock.wait()

			# reset numControlToUpdate and numVehicleToUpdate after waiting
			self.numControlToUpdate = len(self._gvList)
			self.numVehicleToUpdate = len(self._gvList)
			self.simulator_lock.release() # End of Conditinal Critical Region


			#[DEBUG] delay run speed of program to read print statements
			#time.sleep(1)

		if self.__displayClient:
			self.__displayClient.traceOff()
			self.__displayClient.clear()
		print 'Cleared\n'

# Simulator main method called when Simulator.py is executed directly
if __name__ == '__main__':


		# check for proper syntax
		if len(sys.argv) != 3:
			raise IllegalArgumentException("Usage: Simulator <numVehicles> <hostname>\n"+
				"where <numVehicles> is number of vehicles to run in Simulation\n"+
				"where <hostname> is where the DisplayServer is running")
			sys.exit()

		numVehicles = int(sys.argv[1])
		host = sys.argv[2]

		dc = DisplayClient(host)
		sim = Simulator(dc)

		leaderType = 1 #  0: RandomController, 1: LeadingController
		if numVehicles == 1: leaderType = 0 # protection in case only one vehicles

		leader = None
		fc = None # First controller

		for i in range(numVehicles):
			initialPos = ([random.random()*100,random.random()*100,
						random.random()*2.0*math.pi - math.pi])
			speed = random.random()*5.0 + 5.0
			initialDX = speed*math.cos(initialPos[2])
			initialDY = speed*math.sin(initialPos[2])

			initialOmega = random.random()*math.pi/2 - math.pi/4

			gvf = GroundVehicle(initialPos, initialDX, initialDY, initialOmega)
			vc = None # null vehicle controller


			if i == 0:
				if leaderType == 0:
					vc = RandomController(sim,gvf)
				elif leaderType == 1:
					vc = LeadingController(sim,gvf)

				fc = vc # 1st controller is the now defined vc
				leader = gvf 

			else:
				if leader is not None:
					vc = FollowingController(sim,gvf,leader)
					if leaderType == 1:
						fc.addFollower(gvf)

				else:
					print "ERROR: No leader defined."
					sys.exit()

			gvf.addSimulator(sim)
			sim.addGroundVehicle(gvf)
			vc.start()
			gvf.start()

		sim.start()
		sim.join()
