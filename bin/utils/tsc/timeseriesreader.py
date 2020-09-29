import sys, numpy as np
sys.path.append('./')
from bin.utils.tsc.bitbuffer import BitBuffer
from bin.utils.tsc.timereader import TimeReader
from bin.utils.tsc.valuereader import ValueReader
class TimeSeriesReader(object):
    def __init__(self, bytesBuffer = None, bitnum = 64):
        """
        bitnum为数据类型，32为float32，64为float64
        """
        self._buffer = BitBuffer(bytesBuffer)
        self._dateReader = TimeReader(self._buffer)
        self._valueReader = ValueReader(self._buffer, bitnum)


    def HasMorePoints(self):
        return self._dateReader.HasMoreValues()

    def ReadNext(self):
        return self._dateReader.ReadNextTimeStamp(), self._valueReader.ReadNextValue()

    def ReadAll(self):
        timearr = []
        varr = []
        while(self.HasMorePoints()):
            t,v = self.ReadNext()
            timearr.append(t)
            varr.append(v)
        return timearr, varr


if __name__ == "__main__":
    import pickle
    data = pickle.load(open('test.pkl','rb'))
    with open('test.dat', 'rb') as f:
        bs = f.read()
    tsr = TimeSeriesReader(bs, 32)

    i = 0
    rt, rv = tsr.ReadAll()
    print(len(rt), len(data))
    

