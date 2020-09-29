import sys
sys.path.append('./')
from bin.utils.tsc.bitbuffer import BitBuffer
from bin.utils.tsc.timewriter import TimeWriter
from bin.utils.tsc.valuewriter import ValueWriter
class TimeSeriesWriter(object):
    def __init__(self, bitnum = 64):
        """
        bitnum为数据类型，32为float32，64为float64
        """
        self._buffer = BitBuffer(None)
        self._dateWriter = TimeWriter(self._buffer)
        self._valueWriter = ValueWriter(self._buffer, bitnum)


    def AddPoint(self, intTimeStamp, value):
        if (self._dateWriter.AppendTimeStamp(intTimeStamp)):
            self._valueWriter.AppendValue(value)
            return True
        return False

    def ToBytes(self):
        return self._buffer.ToBytes()

    def Save(self, filename):
        with open(filename, 'wb') as f:
            f.write(self._buffer.ToBytes())

if __name__ == "__main__":
    import datetime, random, time
    random.seed(0)
    ts = TimeSeriesWriter(32)
    tnow = datetime.datetime.now()
    num = 3600
    data = []
    val = 0
    for i in range(num):
        tstring = tnow.strftime("%Y-%m-%d %H:%M:%S")
        val += random.random()
        tval = time.mktime(time.strptime(tstring, "%Y-%m-%d %H:%M:%S"))
        ts.AddPoint(tval, val)
        tnow += datetime.timedelta(seconds = -2 + float(random.randint(-100,100))/1000 )
        data.append([tval, val])
    import pickle
    pickle.dump(data, open('test.pkl', 'wb'))
    with open('test.dat', 'wb') as f:
        f.write(ts.ToBytes())
        
    print(ts._buffer._length/num)
    

