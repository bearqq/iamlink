#!/usr/bin/python
import sys
sys.path.append(sys.path[0]+"/core")
sys.path.append(sys.path[0]+"/plugins")
import time
import new
import thread

pluginList = []
forwardQueue = []
ecode = 0

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

while ecode == 0:
    time.sleep(1)
    while forwardQueue:
        thePacket = forwardQueue.pop(0)
        for pq in pluginList:
            if cmp(pq.keyword, thePacket.dstKeyword) == 0:
                pq.recvQueue.append(thePacket)
