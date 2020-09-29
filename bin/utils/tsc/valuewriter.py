import sys, numpy as np
from bin.utils.tsc.bitbuffer import BitBuffer
from bin.utils.tsc.blockinfo import BlockInfo
from bin.utils.tsc.constants import Constants

class ValueWriter(object):
    def __init__(self, bitBuffer, bitnum = 64):
        self._buffer = bitBuffer
        self._previousBlockInfo = None #BlockInfo(0, 0)
        self._previousValue = 0
        self._bitnum = bitnum
        if bitnum == 32:
            self.numfunc = np.float32
            self.parsefunc = np.uint32
        elif bitnum == 64:
            self.numfunc = np.double
            self.parsefunc = np.uint64

    def AppendValue(self, value):
        """
        /// Doubles are encoded by XORing them with the previous value.  If
        /// XORing results in a zero value (value is the same as the previous
        /// value), only a single zero bit is stored, otherwise 1 bit is
        /// stored. 
        ///
        /// For non-zero XORred results, there are two choices:
        ///
        /// 1) If the block of meaningful bits falls in between the block of
        ///    previous meaningful bits, i.e., there are at least as many
        ///    leading zeros and as many trailing zeros as with the previous
        ///    value, use that information for the block position and just
        ///    store the XORred value.
        ///
        /// 2) Length of the number of leading zeros is stored in the next 5
        ///    bits, then length of the XORred value is stored in the next 6
        ///    bits and finally the XORred value is stored.
        """
        longValue = int(np.frombuffer(self.numfunc(value).tobytes(), dtype=self.parsefunc)[0])
        xorWithPrevious = self._previousValue ^ longValue

        if (xorWithPrevious == 0):
            # It's the same value.
            self._buffer.AddValue(0, 1)
            return

        self._buffer.AddValue(1, 1)

        currentBlockInfo = BlockInfo.CalulcateBlockInfo(xorWithPrevious)
        expectedSize = Constants.LeadingZerosLengthBits + Constants.BlockSizeLengthBits + currentBlockInfo.BlockSize

        if  (not self._previousBlockInfo is None) and\
            currentBlockInfo.LeadingZeros >= self._previousBlockInfo.LeadingZeros and\
            currentBlockInfo.TrailingZeros >= self._previousBlockInfo.TrailingZeros and\
            self._previousBlockInfo.BlockSize < expectedSize:
            # Control bit saying we should use the previous block information
            self._buffer.AddValue(1,1)

            # Write the parts of the value that changed.
            blockValue = xorWithPrevious >> self._previousBlockInfo.TrailingZeros
            self._buffer.AddValue(blockValue, self._previousBlockInfo.BlockSize)
        else:
            # Control bit saying we need to provide new block information
            self._buffer.AddValue(0, 1)

            # Details about the new block information
            self._buffer.AddValue(currentBlockInfo.LeadingZeros, Constants.LeadingZerosLengthBits)
            self._buffer.AddValue(currentBlockInfo.BlockSize - Constants.BlockSizeAdjustment, Constants.BlockSizeLengthBits)

            # Write the parts of the value that changed.
            blockValue = xorWithPrevious >> currentBlockInfo.TrailingZeros
            self._buffer.AddValue(blockValue, currentBlockInfo.BlockSize)

            self._previousBlockInfo = currentBlockInfo

        self._previousValue = longValue

    
