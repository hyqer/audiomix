import numpy as N
import wave
import bitarray
import os
def get_signal_data(frequency=440, duration=1, volume=32000, samplerate=44100):
    """Outputs a numpy array of intensities"""
    samples = duration * samplerate
    period = samplerate / float(frequency)
    omega = N.pi * 2 / period
    t = N.arange(samples, dtype=N.float)
    y = volume * N.sin(t * omega)
    print "samples = ",samples,"period = ",period,"omega = ",omega,"t = ",t[:20],"y = ",y[:20]
    return y
def one(direction):
    samples = 12
    t = N.arange(samples, dtype=N.float)
    #print t
    y = direction*32000*N.sin(t*(N.pi/6.0))
    #print "one",y
    #signal = "".join((wave.struct.pack('h', item) for item in y))
    return y
def zero(direction):
    samples = 12
    t = N.arange(samples, dtype=N.float)
    #print t
    y = direction*32000*N.sin(t*(N.pi/3.0))
    #print "zero",y
    #signal = "".join((wave.struct.pack('h', item) for item in y))
    return y
def numpy2string(y):
    """Expects a numpy vector of numbers, outputs a string"""
    signal = "".join((wave.struct.pack('h', item) for item in y))
    # this formats data for wave library, 'h' means data are formatted
    # as short ints
    #print signal[:50],len(signal)
    return signal

class DataFile:
    def __init__(self,sourcefile, filename,samplerate=22050):#44100
        self.file = wave.open(filename, 'wb')
        self.sourcefile = sourcefile
        self.filesize = os.path.getsize(sourcefile)
        self.file.setparams((1, 2, samplerate, (self.filesize+3+len(sourcefile))*9*12, 'NONE', 'noncompressed'))
    def get_signal_data(self,bytes):
        signallist=[]
        for b in bytes:
            ba = bitarray.bitarray()
            ba.fromstring(b)
            sum=0
            
            for bit in ba:
                if bit:
                    sum+=1
                    signallist.extend(one(1))
                else:
                    signallist.extend(zero(1))
            if sum%2:
                signallist.extend(one(1))
            else:
                signallist.extend(zero(1))
        return numpy2string(signallist)
    def _write(self,bytes):
        signal=self.get_signal_data(bytes)
        self.file.writeframes(signal)
    def write(self):
        head = '\x55'
        self._write(head)
        self._write(self.sourcefile)
        self._write('\r\n')
        sf = open(self.sourcefile,'rb')
        self._write(sf.read())
    def close(self):
        self.file.close()
        
        

if __name__ == '__main__':
    print one(1)
    print zero(1)
    df = DataFile('ab1.txt', 'ab1.wav')
    df.write()
    df.close()
    exit()
    print 'file written'
