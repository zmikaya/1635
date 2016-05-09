#ZeroRPC Client
import zerorpc

from Simulator import *

class StreamingRPC(object):
    
    def startSimulator(self):
        mainRun(1)

    
s = zerorpc.Server(StreamingRPC)
s.bind("tcp://0.0.0.0:4242")
s.run()