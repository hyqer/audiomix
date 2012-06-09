import wave
DIR = -1
ONE_GATE=100
class DataFileReader:
    def __init__(self,sf):
        self.file=wave.open(sf,'rb')
        assert(self.file.getnchannels()==1)
        assert(self.file.getsampwidth()==2)
        assert(self.file.getcomptype()=='NONE')
    def printHead(self):
        i=0
        while True:
            data = self.file.readframes(1)
            vol,=wave.struct.unpack("h",data)
            print i,vol
            i+=1
            if i>30:
                break
    def getCycleFrames(self):
        frames = 0
        vol = 0
        while True:
            #print "skip frame"
            data = self.file.readframes(1)
            if not data:
                break
            vol,=wave.struct.unpack("h",data)
            vol = DIR*vol######+-
            #print "v1",vol
            if vol>ONE_GATE:
                break
        frames +=1
        while True:
            data=self.file.readframes(1)
            if not data:
                break
            vol,=wave.struct.unpack("h",data)
            vol = DIR*vol
            frames +=1
            #print "v2",vol
            if vol<ONE_GATE:
                break
        while True:
            data=self.file.readframes(1)
            if not data:
                break
            vol,=wave.struct.unpack("h",data)
            vol = DIR*vol
            #print "v3",vol
            frames +=1
            if vol>-ONE_GATE:
                break
        #print "s=",frames
        return frames
    def getBit(self):
        s = self.getCycleFrames()
        #print "s=",s############6,12cycle
        if s in (6,7):
            s=self.getCycleFrames()
            if s in (5,6,7):
                return 0
        elif s in ( 10,11,12,13,14):
            return 1
        return -1
    def getHead(self):
        for n in xrange(9):
            print "n=",n
            if n%2 !=self.getBit():
                return False
        return True
    def getChar(self):
        byte=0
        sum=0
        for n in xrange(8):
            bit = self.getBit()
            if bit == -1:
                return
            byte += bit*(2**(7-n))
            sum += bit
        bit = self.getBit()
        assert(sum%2==bit)
        return chr(byte)
    def getFileName(self):
        filename=[]
        byte=self.getChar()
        while byte!='\r':
            filename.append(byte)
            byte=self.getChar()
        if self.getChar()=='\n':
            return "".join(filename)
    def close(self):
        self.file.close()
f = DataFileReader("testlua.wav")
#f.printHead()
if not f.getHead():
    print "error file"
    exit()
fileout=f.getFileName()
fo=open(fileout,"wb")
while True:
    c=f.getChar()
    if c:
        fo.write(c)
    else:
        break
fo.close()
f.close()
 