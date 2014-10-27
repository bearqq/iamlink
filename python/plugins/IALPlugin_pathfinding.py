# -*- coding: utf-8 -*-
import thread
import time
from urllib import urlopen
from urllib import quote
import json
import re
from IALCmdPacket import *

class pfTicket:

    def __init__(self, tktSrc, origin, dest, issug, suglist, sugchoice, finalpath, times):
        self.tktSrc = tktSrc
        self.origin = origin
        self.dest = dest
        self.issug = issug
        self.suglist = suglist
        self.sugchoice = sugchoice
        self.finalpath = finalpath
        self.times = times

class IALPlugin_pathfinding:

    ecode = 0
    __sid = "e46jlg03vw2t6ff0"
    name = "pathfinding"
    keyword = ["pathfinding", "path", "寻路"]
    sendQueue = []
    recvQueue = []
    procQueue = {}
    uncompQueue = {}

    __AK = ""
    __MODE = "transit"
    __REGION = ""
    #__ORIGIN_REGION = ""
    #__DESTINATION_REGION = ""
    __OUTPUT = "json"
    #__COORD_TYPE = ""
    #__WAYPOINTS = ""
    __TACTICS = "11"
    #__CONFIDENCE = "0"

    __url_geocoder = "http://api.map.baidu.com/geocoder/v2/?"
    __url_direction = "http://api.map.baidu.com/direction/v1?"
    __url_place = "http://api.map.baidu.com/place/v2/suggestion?"

    def __getsug(self, loc):
        ret = []
        url = self.__url_place + "query=" + loc + "&region=" + self.__REGION + "&output=" + self.__OUTPUT + "&ak=" + self.__AK
        jsonobj = urlopen(url).read()
        suginfo = json.loads(jsonobj, encoding="UTF-8")
        if suginfo.has_key("result"):
            for sug in suginfo["result"]:
                if sug.has_key("name") and sug.has_key("city"):
                    if sug["city"]:
                        ret.append(sug["name"].encode("utf-8"))
        if not ret or suginfo["status"]:
            ret = 0
        return ret

    def __getcood(self, loc):
        ret = 0
        url = self.__url_geocoder + "address=" + loc + "&city=" + self.__REGION + "&output=" + self.__OUTPUT + "&ak=" + self.__AK
        jsonobj = urlopen(url).read()
        coodinfo = json.loads(jsonobj)
        if coodinfo.has_key("result"):
            if coodinfo["result"].has_key("location"):
                ret = str(coodinfo["result"]["location"]["lat"]) + "," + str(coodinfo["result"]["location"]["lng"])
        return ret

    def __getpath(self, origincood, destcood):
        ret = []
        url = self.__url_direction + "mode=" + self.__MODE + "&origin=" + origincood + "&destination=" + destcood + "&region=" + self.__REGION + "&tactics=" + self.__TACTICS + "&output=" + self.__OUTPUT + "&ak=" + self.__AK
        jsonobj = urlopen(url).read()
        pathinfo = json.loads(jsonobj)
        if pathinfo.has_key("result"):
            if pathinfo["result"].has_key("routes"):
                i = 0
                for route in pathinfo["result"]["routes"]:
                    for scheme in route["scheme"]:
                        i += 1
                        ret.append("Plan" + str(i) + ":")
                        for stepsP in scheme["steps"]:
                            for steps in stepsP:
                                if steps.has_key("stepInstruction"):
                                    tstr = re.sub("<[/]?b>|<[/]?font.*?(t|\")?>", "", steps["stepInstruction"])
                                    ret.append(tstr.encode("utf-8"))
        if not ret or pathinfo["status"]:
            ret = 0
        return ret
                        

    def __pathfinding(self, origin, dest):
        ret = []
        origincood = self.__getcood(origin)
        if not origincood:
            sug = self.__getsug(origin)
            if not sug:
                ret.append(3)
                ret.append("Wrong Origin")
            else:
                ret.append(1)
                ret.append(sug)
            return ret
        destcood = self.__getcood(dest)
        if not destcood:
            sug = self.__getsug(dest)
            if not sug:
                ret.append(3)
                ret.append("Wrong Dest")
            else:
                ret.append(2)
                ret.append(sug)
            return ret
        thepath = self.__getpath(origincood, destcood)
        if not thepath:
            ret.append(4)
            ret.append("No Path Available")
            return ret
        ret.append(0)
        ret.append(thepath)
        return ret

    def __tickethandler(self):
        cmd = ""
        while not self.ecode:
            time.sleep(1)
            while self.procQueue:
                for (k, v) in self.procQueue.items():
                    if not v.times:
                        cmd = "Try other locations"
                    else:
                        ret = self.__pathfinding(v.origin, v.dest)
                        if ret[0] == 1:
                            v.suglist = ret[1]
                            v.issug = 1
                            cmd = "choose origin:"
                            i = 0
                            for tstr in ret[1]:
                                i += 1
                                cmd += str(i) + "." + tstr
                            self.uncompQueue[k] = v
                        elif ret[0] == 2:
                            v.suglist = ret[1]
                            v.issug = 2
                            cmd = "choose dest:"
                            i = 0
                            for tstr in ret[1]:
                                i += 1
                                cmd += str(i) + "." + tstr
                            self.uncompQueue[k] = v
                        else:
                            for tstr in ret[1]:
                                cmd += tstr
                    self.__send(v.tktSrc, cmd)
                    cmd = ""
                    del self.procQueue[k]
            

    def __uncomphandler(self):
        while not self.ecode:
            time.sleep(1)
            while self.uncompQueue:
                time.sleep(1)
                for (k, v) in self.uncompQueue.items():
                    if v.sugchoice > len(v.suglist):
                        v.sugchoice = len(v.suglist)
                    if v.sugchoice:
                        if v.issug == 1:
                            v.origin = v.suglist[v.sugchoice-1]
                        elif v.issug == 2:
                            v.dest = v.suglist[v.sugchoice-1]
                        v.issug = 0
                        v.sugchoice = 0
                        v.times -= 1
                        self.procQueue[k] = v
                        del self.uncompQueue[k]
        

    def __send(self, dst, cmd):
        #print "IALPlugin_pathfinding Send Reply \"" + cmd + "\" to " + dst
        tpkt = IALCmdPacket("pathfinding", dst, "", cmd, self.__sid)
        self.sendQueue.append(tpkt)

    def __main(self):
        thread.start_new_thread(self.__recv, ())
        thread.start_new_thread(self.__tickethandler, ())
        thread.start_new_thread(self.__uncomphandler, ())

    def __recv(self):
        while not self.ecode:
            time.sleep(1)
            while self.recvQueue:
                thePacket = self.recvQueue.pop(0)
                #print "IALPlugin_pathfinding Recv \"" + thePacket.cmd + "\" From " + thePacket.src
                if self.uncompQueue.has_key(thePacket.sid):
                    self.uncompQueue[thePacket.sid].sugchoice = int(thePacket.cmd)
                else:
                    tcmd = thePacket.cmd.split(' ', 2)
                    if len(tcmd) == 3 and tcmd[2]:
                        self.__REGION = tcmd[0]
                        tmpt = pfTicket(thePacket.src, tcmd[1], tcmd[2], 0, [], 0, [], 3)
                        self.procQueue[thePacket.sid] = tmpt

    def launch(self):
        self.__main()
