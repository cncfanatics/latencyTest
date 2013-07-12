from twisted.internet import reactor
from txzmq import ZmqDealerConnection, ZmqFactory, ZmqEndpoint, ZmqEndpointType
from twisted.internet.task import LoopingCall
import time
import sys
import argparse

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('socket', type=str)
parser.add_argument('--burstTime', help='Amount of time between bursts', default=0.1, type=float)
parser.add_argument('--burstAmount', help='Amount of packets to burst', default=10, type=int)
args = parser.parse_args()
sys.stdout.write("Starting up at bursts of {} every {} seconds\n\r".format(args.burstAmount, args.burstTime))


class Sender(ZmqDealerConnection):
    def __init__(self, factory, endpoint, identity='sender'):
        super(Sender, self).__init__(factory, endpoint, identity=identity)
        self.iteration = 1
        self.times = {}
        self.totalReceived = 0
        self.totalTime = 0
        self.roundTime = time.time()

        self.lc = LoopingCall(self.burst)
        self.lc.start(args.burstTime)

        self.lc = LoopingCall(self.displayAvg)
        self.lc.start(1, now=False)

    def burst(self):
        iteration = self.iteration
        for i in xrange(args.burstAmount):
            self.times[(iteration, i)] = time.time()
            self.send(['pong', str(iteration), str(i)])

        self.iteration += 1

    def gotMessage(self, msgType, iteration, i):
        if self.totalReceived >= 10000:
            sys.stdout.write("\rPing: {} ==> {}s for {} messages (Queued: {})\n".format(self.totalTime / self.totalReceived, time.time() - self.roundTime, self.totalReceived, len(self.times)))
            self.totalReceived = 0
            self.totalTime = 0
            self.roundTime = time.time()

        currTime = time.time()
        k = int(iteration), int(i)
        RTT = (currTime - self.times[k]) * 1000
        self.totalTime += RTT
        self.totalReceived += 1
        del self.times[k]

    def displayAvg(self):
        if self.totalReceived:
            sys.stdout.write("\rPing: {} Waiting messages: {} ({} / {})     ".format(self.totalTime / self.totalReceived, len(self.times), self.totalTime, self.totalReceived))


zf = ZmqFactory()
s = Sender(zf, ZmqEndpoint(ZmqEndpointType.connect, parser.socket))
reactor.run()
