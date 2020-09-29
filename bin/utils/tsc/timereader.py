
from bin.utils.tsc.bitbuffer import BitBuffer
from bin.utils.tsc.constants import Constants
from bin.utils.tsc.timestampencodingdetails import TimestampEncodingDetails
class TimeReader(object):
    def __init__(self, bitBuffer):
        self._buffer = bitBuffer
        self._hasReadFirstValue = False

    def HasMoreValues(self):
        return not self._buffer.IsAtEndOfBuffer()

    def ReadNextTimeStamp(self):
        if (self._hasReadFirstValue == False):
            timestamp = self._buffer.ReadValue(Constants.BitsForFirstTimestamp)
            self._previousTimestamp = timestamp
            self._previousTimestampDelta = Constants.DefaultDelta
            self._hasReadFirstValue = True
            return timestamp
        
        vtype = self._buffer.FindTheFirstZeroBit(TimestampEncodingDetails.MaxControlBitLength)

        if (vtype > 0):
            index = vtype - 1
            encoding = TimestampEncodingDetails.Encodings[index]

            decodedValue = self._buffer.ReadValue(encoding.BitsForValue)
            
            decodedValue -= encoding.MaxValueForEncoding

            if (decodedValue >= 0):
                decodedValue += 1

            self._previousTimestampDelta += decodedValue
        
        self._previousTimestamp += self._previousTimestampDelta
        return self._previousTimestamp