import thread
from IALCmdPacket import *

class IALPlugin_light:
    ecode = 0
    name = "light"
    keyword = "light"
    sendQueue = []
    recvQueue = []

    def __send(self, dst, cmd):
        print "IALPlugin_light Send Reply " + cmd + " to " + dst
        tpkt = IALCmdPacket("light", dst, dst, cmd)
        self.sendQueue.append(tpkt)

    def __main(self):
        thread.start_new_thread(self.recv, ())
        #while self.ecode == 0:
            

    def recv(self):
        while self.ecode == 0:
            while self.recvQueue:
                thePacket = self.recvQueue.pop(0)
                print "IALPlugin_light Recv: " + thePacket.cmd
                self.__send(thePacket.src, thePacket.cmd)

    def launch(self):
        self.__main()
