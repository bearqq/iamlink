# -*- coding: utf-8 -*-
import thread
from IALCmdPacket import *

class IALPlugin_sender:
    ecode = 0
    name = "sender"
    keyword = "sender"
    sendQueue = []
    recvQueue = []

    def __send(self, dst, cmd):
        print "IALPlugin_sender Send " + cmd + " to " + dst
        tpkt = IALCmdPacket("sender", dst, dst, cmd)
        self.sendQueue.append(tpkt)

    def __main(self):
        thread.start_new_thread(self.recv, ())
        while self.ecode == 0:
            uinput = raw_input("\n您想要做什么：")
            if uinput:
                tstr = uinput.split(' ', 1)
                if len(tstr) == 2 and tstr[1]:
                    self.__send(tstr[0], tstr[1])

    def recv(self):
        while self.ecode == 0:
            while self.recvQueue:
                thePacket = self.recvQueue.pop(0)
                print "IALPlugin_sender Recv: " + thePacket.cmd

    def launch(self):
        self.__main()
