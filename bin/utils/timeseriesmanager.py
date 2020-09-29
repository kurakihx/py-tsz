import sys, os, time
sys.path.append('./')
from bin.utils.tsc.timeseriesreader import TimeSeriesReader
from bin.utils.tsc.timeserieswriter import TimeSeriesWriter
from bin.utils.memdata import MemData

class TimeSeriesManager(object):
    """
    """
    def __init__(self):
        self._writer = {}

    def _timeStampToString(self, timestamp):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

    def _timeStringToStamp(self, tstring):
        tstring = tstring.strip()
        if len(tstring) == 10:
            return int(time.mktime(time.strptime(tstring, '%Y-%m-%d')) * 1000)
        elif len(tstring) == 19:
            return int(time.mktime(time.strptime(tstring, '%Y-%m-%d %H:%M:%S')) * 1000)
        elif len(tstring) == 21:
            return int(time.mktime(time.strptime(tstring[:19], '%Y-%m-%d %H:%M:%S')) * 1000 + int(tstring[20:]) * 100)
        elif len(tstring) == 22:
            return int(time.mktime(time.strptime(tstring[:19], '%Y-%m-%d %H:%M:%S')) * 1000 + int(tstring[20:]) * 10)
        elif len(tstring) == 23:
            return int(time.mktime(time.strptime(tstring[:19], '%Y-%m-%d %H:%M:%S')) * 1000 + int(tstring[20:]))

    def AddPoint(self, timestring, pointnames, pointvalues):
        """
        timestring:yyyy-mm-dd/yyyy-mm-dd hh:MM:ss/yyyy-mm-dd hh:MM:ss.fff
        pointvalues:[{pointname1:value1},{{pointname2:value1}}]
        """
        daykey = timestring[:10]
        datatimestamp = self._timeStringToStamp(timestring)
        if not daykey in self._writer:
            self._writer[daykey] = {}
        for pointname, pointvalue in zip(pointnames, pointvalues):
            if pointname in self._writer[daykey]:
                self._writer[daykey][pointname].AddPoint(datatimestamp, pointvalue)
            else:
                twriter = self._newWriter(daykey, pointname)
                self._writer[daykey][pointname] = twriter
                twriter.AddPoint(datatimestamp, pointvalue)

    def _newWriter(self, todaykey, pointname):
        #先判断./data/yyyy/mm/dd/pointname文件是否存在
        ele = todaykey.split('-')
        filename = './data/%s/%s/%s/%s.dat' % (ele[0],ele[1], ele[2], pointname)
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                reader = TimeSeriesReader(f.read())
                times, values = reader.ReadAll()
                return MemData(times, values)
        else:
            return MemData([],[])

    def Flush(self):
        """
        将数据写入文件，并将旧内存数据删除
        """
        todayhour = int(self._timeStampToString(time.time())[11:13])
        todaykey = self._timeStampToString(time.time())[:10]
        todeletekey = []
        for dw in self._writer.keys():
            ele = dw.split('-')
            basedir = './data/%s/%s/%s/' % (ele[0],ele[1], ele[2])
            if not os.path.exists(basedir):
                os.makedirs(basedir)
            for rw in self._writer[dw]:
                filename = './data/%s/%s/%s/%s.dat' % (ele[0],ele[1], ele[2], rw)
                tsw = TimeSeriesWriter()
                for t,v in zip(self._writer[dw][rw].timeStamp, self._writer[dw][rw].value):
                    tsw.AddPoint(t, v)
                tsw.Save(filename)
            if dw != todaykey:
                todeletekey.append(dw)
        if todayhour > 1:
            #1点后删除不是当天的内存数据
            for dw in todeletekey:
                self._writer.pop(dw)

if __name__ == "__main__":
    a =  TimeSeriesManager()
    a.AddPoint('2020-09-27 11:33:46.456', ['p1','p2'], [1.24,2.35])
    a.Flush()