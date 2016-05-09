#ZeroRPC Client
import zerorpc

from Simulator import *

class StreamingRPC(object):
    def __init__(self, sim):
        self.sim = sim

    def getSim(self):
        return self.sim

    def startSim():
        self.sim.start()

    def getPositionFromSim():
        return [self.sim.apX, self.sim.apY, self.sim.apZ]

    
