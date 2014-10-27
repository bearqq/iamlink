class IALCmdPacket:

    def __init__(self, src, dst, dstKeyword, cmd, sid):
        self.src = src
        self.dst = dst
        self.dstKeyword = dstKeyword
        self.cmd = cmd
        self.sid = sid
