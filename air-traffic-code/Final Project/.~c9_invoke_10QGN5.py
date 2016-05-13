# Simulator.py
# Assignment 3

# Author: Frederick Daso

import math, sys, threading, time, random

from IllegalArgumentException import *
from FollowingController import *
from PlaneController import *
from LeadingController import *
from RandomController import *
from UserController import *
from Airplane import *
from DisplayClient import *
from Control import *
import zerorpc
import json
from pymongo import MongoClient

class Simulator(threading.Thread):

	def __init__(self, displayClient=None, stream=False):
		threading.Thread.__init__(self)
    
		self._stream = stream
		self._zerorpc_client = zerorpc.Client()
		self._zerorpc_client.connect("tcp://127.0.0.1:4242")
		
		self.db_ip = 'localhost'
		self.db_port = 8081
		client = MongoClient(self.db_ip, self.db_port)
		meteor_db = client.meteor
		self.aircraft_collection = meteor_db.aircraft
        
		self.__currentSec = 0
		self.__currentMSec = 0
		self.apX = []
		self.apY = []
		self.apZ = []
		self.apTheta = []
		
		self.duration = 30
		self.halt = False

		# NOTE: the '_' prefix is python convention, and does not 
		# affect the behavior of the targeted member 
		# (in this case, '_apList' will behave identically to 'apList')
		self._apList = [] # 'protected' class member

		# if displayClient is None:
		# 	print 'WARNING: No DisplayClient specified'
		# 	pass
		self.__displayClient = displayClient
				
		# Non-Private class members
		self.numControlToUpdate = 0
		self.numPlaneToUpdate = 0

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

	def addAirplane(self, ap):
		self.simulator_lock.acquire() # start critical region
		self._apList.append(ap)
		print "---------Adding Ground Plane-----------\n"
		i = 1
		for ap in self._apList:
			pos = ap.getPosition()
			print "%i : %f,%f,%f" %  (i,pos[0],pos[1],pos[2])
			i+=1
		print " "

		self.numControlToUpdate += 1
		self.numPlaneToUpdate += 1
		self.simulator_lock.release() # end critical region
		
	def set_db_coords(self, player_id, coords):
		self.aircraft_collection.update_one(
			{'_id': player_id},
			{'$set': {'x-pos': coords[0], 'y-pos': coords[1], 'z-pos': coords[2]}},
			upsert=True
		)
		
	def set_db_angles(self, player_id, angles):
		self.aircraft_collection.update_one(
			{'_id': player_id},
			{'$set': {'pitch': angles[0], 'roll': angles[1]}},
			upsert=True
		)
		
	def haltSystem(self):
		self.halt = True
		
	def get_player_ids(self):
		player_ids = [el.values()[0] for el in self.aircraft_collection.find({}, {'_id': 1})]
		return player_ids

	def run(self):

		# We're going to need these to know how much time has elapsed since the
		# last call to vehicle.updateState(). We could leave this out, and always
		# call vehicle.updateState() with arguments of 0 and 10, but for a
		# real-time implementation in a later assignment, we're actually going to
		# need to measure the elapsed time. 
		
		# self.set_db_coords('b2', [300, 300, 300])
		# self.set_db_angles('b2', [0, 0])
		
		lastUpdateSec = self.__currentSec
		lastUpdateMSec = self.__currentMSec

		if self.__displayClient:
			self.__displayClient.clear()
			self.__displayClient.traceOn()

		print "Simulator thread started"

		while (self.__currentSec < self.duration) and not self.halt:
			#[NOT NECESSARY] Implemented for convenience of having the VC and 
			# Sim threads ends when quit is called on the DisplayServer
		# 	if not self.__displayClient.isConnected():
		# 		print 'SIM: display client NOT connected'
		# 		break

			deltaSec = self.__currentSec - lastUpdateSec
			deltaMSec = self.__currentMSec - lastUpdateMSec

			if (deltaMSec < 0):
				deltaMSec += 1e3
				deltaSec -= 1

			apX = []
			apY = []
			apTheta = []

			# populate data to be sent to display client 
			for currentAP in self._apList:
				pos = currentAP.getPosition()
				vel = currentAP.getVelocity()
				apX.append(pos[0])
				self.apX.append(pos[0])
				apY.append(pos[1])
				self.apY.append(pos[1])
				self.apZ.append(pos[2])
				apTheta.append(pos[3])
				self.apTheta.append(pos[3])
				player_id = currentAP.player_id
				self.set_db_coords(player_id, [self.apX[-1], self.apY[-1], self.apZ[-1]])
				print 'id: {0}; x: {1}; y: {2}; z: {3}'.format(player_id, self.apX[-1], self.apY[-1], self.apZ[-1])
			

			# send AP positions to the DisplayServer using the DisplayClient
		# 	if self.__displayClient:
		# 		self.__displayClient.update(len(self._apList),apX,apY,apTheta)
		

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
				if self.numControlToUpdate == 0 and self.numPlaneToUpdate == 0:
					break
				self.simulator_lock.wait()

			# reset numControlToUpdate and numPlaneToUpdate after waiting
			self.numControlToUpdate = len(self._apList)
			self.numPlaneToUpdate = len(self._apList)
			self.simulator_lock.release() # End of Conditinal Critical Region
			
			# check db if this should be running
			# self.halt = self.aircraft_collection.find_one({'_id': })['halt']

			#[DEBUG] delay run speed of program to read print statements
			#time.sleep(1)

		if self.__displayClient:
			self.__displayClient.traceOff()
			self.__displayClient.clear()
		print 'Cleared\n'
		
def mainRun():

	sim = Simulator()
	
	player_ids = sim.get_player_ids()
	numPlanes = len(player_ids)

	for i in range(numPlanes):
		player_id = player_ids[i]
		initialPos = ([300, 300, 300, 0, 0])
		speed = random.random()*5.0 + 5.0
		initialDX = speed*math.cos(initialPos[3])
		initialDY = speed*math.sin(initialPos[3])
		initialDZ = speed*math.sin(initialPos[4])

		initialOmegaX = 0
		initialOmegaZ = 0

		apf = Airplane(initialPos, initialDX, initialDY, initialDZ, initialOmegaX, initialOmegaZ, player_id)
		pc = UserController(sim, apf)

		apf.addSimulator(sim)
		sim.addAirplane(apf)
		pc.start()
		apf.start()

	sim.start()
	sim.join()

# Simulator main method called when Simulator.py is executed directly
if __name__ == '__main__':
	
	mainRun()
