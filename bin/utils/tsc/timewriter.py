import time
import sys
from bin.utils.tsc.bitbuffer import BitBuffer
from bin.utils.tsc.blockinfo import BlockInfo
from bin.utils.tsc.constants import Constants
from bin.utils.tsc.timestampencodingdetails import TimestampEncodingDetails
class TimeWriter(object):
    def __init__(self, bitBuffer, minTimeStampDelta = 0):
        # Values coming in faster than this are considered spam
        self._minTimeStampDelta = minTimeStampDelta
        self._buffer = bitBuffer
        self._hasStoredFirstValue = False
        self._previousTimestamp = 0

    def AppendTimeStamp(self, timestamp):
        """
        /// Store a delta of delta for the rest of the values in one of the
        /// following ways
        ///
        /// '0' = delta of delta did not change
        /// '10' followed by a value length of 7
        /// '110' followed by a value length of 9
        /// '1110' followed by a value length of 12
        /// '1111' followed by a value length of 32
        """
        timestamp = int(timestamp)
        delta = timestamp - self._previousTimestamp

        if (delta < self._minTimeStampDelta and self._previousTimestamp != 0):
            return False

        if (self._hasStoredFirstValue == False):
            # Store the first timestamp as it.
            self._buffer.AddValue(timestamp, Constants.BitsForFirstTimestamp)
            self._previousTimestamp = timestamp
            self._previousTimestampDelta = Constants.DefaultDelta
            self._hasStoredFirstValue = True
            return True

        deltaOfDelta = delta - self._previousTimestampDelta

        if (deltaOfDelta == 0):
            self._previousTimestamp = timestamp
            self._buffer.AddValue(0, 1)
            return True

        if (deltaOfDelta > 0):
            # We don't use zero (its handled above).  Shift down 1 so we fit in X number of bits.
            deltaOfDelta -= 1

        absValue = abs(deltaOfDelta)

        for timestampEncoding in TimestampEncodingDetails.Encodings:
            if (absValue < timestampEncoding.MaxValueForEncoding):
                self._buffer.AddValue(timestampEncoding.ControlValue, timestampEncoding.ControlValueBitLength)

                # Make this value between [0, 2^timestampEncodings[i].bitsForValue - 1]
                encodedValue = deltaOfDelta + timestampEncoding.MaxValueForEncoding
                self._buffer.AddValue(encodedValue, timestampEncoding.BitsForValue)
                break

        self._previousTimestamp = timestamp
        self._previousTimestampDelta = delta

        return True