# -*- coding: utf-8 -*-
import thread
import os
from IALCmdPacket import *

class IALPlugin_sender:
    ecode = 0
    name = "sender"
    keyword = ["sender"]
    sendQueue = []
    recvQueue = []
    __sid = "ozblsgowucexqyj7"

    def __send(self, dst, dstKeyword, cmd):
        #print "IALPlugin_sender Send " + cmd + " to " + dstKeyword
        tpkt = IALCmdPacket("sender", dst, dstKeyword, cmd, self.__sid)
        self.sendQueue.append(tpkt)

    def __main(self):
        thread.start_new_thread(self.__recv, ())
        while self.ecode == 0:
            uinput = raw_input("\nWhat do you want to do:")
            if uinput:
                if os.name=='nt':
                    uinput = uinput.decode('gbk')
                else:
                    uinput = uinput.decode('utf-8')
                tstr = uinput.split(' ', 1)
                if len(tstr) == 2 and tstr[1]:
                    self.__send("", tstr[0], tstr[1])

    def __recv(self):
        while not self.ecode:
            while self.recvQueue:
                thePacket = self.recvQueue.pop(0)
                #print "IALPlugin_sender Recv \"" + thePacket.cmd + "\" From " + thePacket.src
                print thePacket.cmd

    def launch(self):
        self.__main()