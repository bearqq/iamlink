# -*- coding: utf-8 -*-
import thread
from IALCmdPacket import *

class IALPlugin_light:
    ecode = 0
    name = "light"
    keyword = ["light", "lamp", "灯"]
    sendQueue = []
    recvQueue = []

    def __send(self, dst, cmd):
        print "IALPlugin_light Send Reply \"" + cmd + "\" to " + dst
        tpkt = IALCmdPacket("light", dst, "", cmd)
        self.sendQueue.append(tpkt)

    def __main(self):
        thread.start_new_thread(self.__recv, ())

    def __recv(self):
        while not self.ecode:
            while self.recvQueue:
                thePacket = self.recvQueue.pop(0)
                print "IALPlugin_light Recv \"" + thePacket.cmd + "\" From " + thePacket.src
                self.__send(thePacket.src, thePacket.cmd)

    def launch(self):
        self.__main()
