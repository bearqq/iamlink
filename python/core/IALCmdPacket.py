class IALCmdPacket:

    def __init__(self, src, dst, dstKeyword, cmd):
        self.src = src
        self.dst = dst
        self.dstKeyword = dstKeyword
        self.cmd = cmd
