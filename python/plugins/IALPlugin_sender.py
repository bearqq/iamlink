# -*- coding: utf-8 -*-
import thread
from IALCmdPacket import *

class IALPlugin_sender:
    ecode = 0
    name = "sender"
    keyword = ["sender"]
    sendQueue = []
    recvQueue = []

    def __send(self, dst, dstKeyword, cmd):
        print "IALPlugin_sender Send " + cmd + " to " + dstKeyword
        tpkt = IALCmdPacket("sender", dst, dstKeyword, cmd)
        self.sendQueue.append(tpkt)

    def __main(self):
        thread.start_new_thread(self.__recv, ())
        while self.ecode == 0:
            uinput = raw_input("\nWhat do you want to do：")
            if uinput:
                tstr = uinput.split(' ', 1)
                if len(tstr) == 2 and tstr[1]:
                    self.__send("", tstr[0], tstr[1])

    def __recv(self):
        while not self.ecode:
            while self.recvQueue:
                thePacket = self.recvQueue.pop(0)
                print "IALPlugin_sender Recv \"" + thePacket.cmd + "\" From " + thePacket.src

    def launch(self):
        self.__main()
