#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append(sys.path[0]+"/core")
sys.path.append(sys.path[0]+"/plugins")
import time
import new
import thread

from IALCmdPacket import *

pluginList = []
forwardQueue = []
keywordIndex = {}
ecode = 0

def makeIndex():
    for pq in pluginList:
        for kd in pq.keyword:
            keywordIndex[kd] = pq.name

tmpmod = __import__('IALPlugin_sender')
tmpclass = getattr(tmpmod, 'IALPlugin_sender')
tmpobj = new.instance(tmpclass)
tmpobj.sendQueue = forwardQueue
pluginList.append(tmpobj)
thread.start_new_thread(tmpobj.launch, ())

tmpmod = __import__('IALPlugin_light')
tmpclass = getattr(tmpmod, 'IALPlugin_light')
tmpobj = new.instance(tmpclass)
tmpobj.sendQueue = forwardQueue
pluginList.append(tmpobj)
thread.start_new_thread(tmpobj.launch, ())

makeIndex()

while not ecode:
    time.sleep(1)
    while forwardQueue:
        thePacket = forwardQueue.pop(0)
        if (not thePacket.dst) and thePacket.dstKeyword:
            thePacket.dst = keywordIndex.get(thePacket.dstKeyword, thePacket.src)
            if not cmp(thePacket.dst, thePacket.src):
                print "Plugin not found, now send pkt back to src"
                thePacket.src = "System"
                thePacket.cmd = "No Such Plugin"
            else:
                print "Plugin found:" + thePacket.dst
        for pq in pluginList:
            if not cmp(pq.name, thePacket.dst):
                pq.recvQueue.append(thePacket)
                break
