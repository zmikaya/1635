# DeadlockTester.py
# Assignment 3

# Author: Alessandro Lira

import thread, threading

from DeadlockTesterException import *

class DeadlockTester:

	# Used to test for potential deadlock scenarios 

	# Checks that the current thread that is trying to access Airplane
	# 'ap' method does not hold a different lock except the built-in lock of
	# 'ap'

	# Args:
	# 	arg1 (Airplane): groundplane that is calling this method
	# 	arg2 (Simulator): simulator in which this Airplane is added

	# Returns:
	# 	bool: True if it doesn't hold any lock (different from built-in 
	# 	lock of 'ap')

	# Raises:
	# 	DeadlockTesterException
	

	@staticmethod
	def testLock(targetap,sim):
		apList = sim._apList # note that sim._apList is psuedo-protected
		for ap in apList:
			# check if current threaad holds each ap's intrinsic lock
			if ap.ap_lock._RLock__owner == thread.get_ident():
				print "Holds Lock to %i" % ap.getplaneID()
				if ap != targetap:
					raise DeadlockTesterException()
					return False
		return True
	

	# ----------------------------------------------------------------------------

	# Alternatively, we could use the methods below to ensure that we acquire
	# locks in a specific order (and release in reverse order). 

	# NOTE: The following methods are not a complete deadlock prevention solution,
	# but are potential building blocks to deadlock prevention system


	# Each plane has a distinct Id. The order to get the locks is
    # from lowest to highest. If this ground plane has a lower id
    # than the leader, it gets its own lock first and then the
    # leaders lock. Else the order to get the locks will be reversed.
	
	# @staticmethod
	# def lockapLocks(apList, ID):
	# 	orderedList = sortplanesByID(apList)
	# 	for ap in orderedList:
	# 		ap.ap_lock.acquire()

    # Unlocks all the 'myapLocks' lock of each Airplane object in the
    # apList.
	
	# @staticmethod
	# def unlockapLocks(apList, ID):
	# 	orderedList = reverseSortplanesByID(apList)
	# 	for ap in orderedList:
	# 		ap.ap_lock.release()


	# Sorting lists in Python
	# Python has built-in list sorting functionality. The mothods written here
	# are merely wrappers for the built in 'sorted' function. Lists of Objects
	# can be sorted by Object attribute (even provate attributes) by providing
	# logic which returns the value of said attrbute in the 'key' argument of 
	# the 'sorted' function

	# @staticmethod
	# def sortVehcilesByID(apList):
	# 	return sorted(apList, key = Airplane.getplaneID)

	# @staticmethod
	# def reverseSortVehcilesByID(apList):
	# 	return sorted(apList, key = Airplane.getplaneID, reverse=True)
				
	# For more info, check here: 
	# https://wiki.python.org/moin/HowTo/Sorting#Key_Functions











