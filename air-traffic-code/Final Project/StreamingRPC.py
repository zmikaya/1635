#ZeroRPC Client
import zerorpc

from Simulator import *

class StreamingRPC(object):
    def __init__(self):
        self.sim = None
    
    def startSimulator(self, val):
        mainRun(1)

    
s = zerorpc.Server(StreamingRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()