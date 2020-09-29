import numpy as np
class MemData(object):
    def __init__(self, times, mems):
        self.timeStamp = times
        self.value = mems

    def AddPoint(self, timestamp, value):
        timestamp = int(timestamp)
        if timestamp in self.timeStamp:
            return
        self.timeStamp.append(timestamp)
        self.value.append(value)
    
    def GetSortList(self):
        nptime = np.array(self.timeStamp, dtype=np.int64)
        npvalue = np.array(self.value)
        sortindex = np.argsort(nptime)
        return nptime[sortindex], npvalue[sortindex]
