import numpy as np
from bin.utils.tsc.bitbuffer import BitBuffer
from bin.utils.tsc.blockinfo import BlockInfo
from bin.utils.tsc.constants import Constants
class ValueReader(object):
    def __init__(self, bitBuffer, bitnum = 64):
        self._buffer = bitBuffer
        self._hasReadFirstValue = False
        self._previousValue = 0
        self._previousBlockInfo = None
        
        if bitnum == 1:
            self.numfunc = np.int8
            self.parsefunc = np.uint64
        elif bitnum == 2:
            self.numfunc = np.int16
            self.parsefunc = np.uint64
        elif bitnum == 4:
            self.numfunc = np.int32
            self.parsefunc = np.uint64
        elif bitnum == 8:
            self.numfunc = np.int64
            self.parsefunc = np.uint64
        elif bitnum == 32:
            self.numfunc = np.float32
            self.parsefunc = np.uint32
        elif bitnum == 64:
            self.numfunc = np.double
            self.parsefunc = np.uint64
        

    def HasMoreValues(self):
        return not self._buffer.IsAtEndOfBuffer()

    def ReadNextValue(self):
        nonZeroValue = self._buffer.ReadValue(1)

        if (nonZeroValue == 0):
            return float(np.frombuffer(self.parsefunc(self._previousValue).tobytes(), dtype=self.numfunc)[0])

        usePreviousBlockInfo = self._buffer.ReadValue(1)
        xorValue = 0

        if (usePreviousBlockInfo == 1):
            xorValue = self._buffer.ReadValue(self._previousBlockInfo.BlockSize)
            xorValue <<= self._previousBlockInfo.TrailingZeros
        else:
            leadingZeros = self._buffer.ReadValue(Constants.LeadingZerosLengthBits)
            blockSize = self._buffer.ReadValue(Constants.BlockSizeLengthBits) + Constants.BlockSizeAdjustment
            trailingZeros = 64 - blockSize - leadingZeros
            xorValue = self._buffer.ReadValue(blockSize)
            xorValue <<= trailingZeros

            self._previousBlockInfo = BlockInfo(leadingZeros, trailingZeros)

        value = xorValue ^ self._previousValue
        self._previousValue = value

        return np.frombuffer(self.parsefunc(value).tobytes(), dtype=self.numfunc)[0]
