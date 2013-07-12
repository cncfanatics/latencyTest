from twisted.internet import reactor
from txzmq import ZmqDealerConnection, ZmqFactory, ZmqEndpoint, ZmqEndpointType
from twisted.internet.task import LoopingCall
import time


class PongSender(ZmqDealerConnection):
    def gotMessage(self, msgType, iteration, i):
        self.sendMultipart(['pong', iteration, i])


zf = ZmqFactory()
s = PongSender(zf, ZmqEndpoint(ZmqEndpointType.bind, 'tcp://*:5555'))
reactor.run()
