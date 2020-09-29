import numpy as np

class BitBuffer(object):
    def __init__(self, bytesBuffer = None, size = 512, startbitnum = 3):
        if bytesBuffer is None:
            self.DefaultBufferSize = size
            self.UnusedBitsInLastByteBitLength = startbitnum    # 3个bit的起始符
            self._capacity = size
            self._buffer = np.zeros(size, dtype=np.uint8)
            self._length = 0     # byte length
            self._numBits = 0    # bit length
            self._bitPostion = self.UnusedBitsInLastByteBitLength

            # Reserve space for the unused bit count
            self.AddValue(0, self.UnusedBitsInLastByteBitLength)
        else:
            self.UnusedBitsInLastByteBitLength = startbitnum    # 3个bit的起始符
            self._length = len(bytesBuffer)
            self._bitPostion = 0
            self._buffer = np.frombuffer(bytesBuffer, dtype=np.uint8)
            unusedBitsInLastByte = self.ReadValue(self.UnusedBitsInLastByteBitLength)
            self._numBits = self._length * 8 - unusedBitsInLastByte
            self._capacity = self._length


    def MoveToStartOfBuffer(self):
        self._bitPostion = self.UnusedBitsInLastByteBitLength

    def ToBytes(self):
        # Update the available bits in the last byte counter stored
        # at the start of the buffer.
        bitsAvailable = self.__BitsAvailableInLastByte()
        bitsUnusedShifted = (bitsAvailable << (8 - self.UnusedBitsInLastByteBitLength))
        self.__SetByteAt(0, (self._buffer[0] | bitsUnusedShifted))

        copy = self._buffer[:self._length].tobytes()
        return copy


    def AddValue(self, value, bitsInValue = 1):
        if (bitsInValue == 0):
            # Nothing to do.
            return

        bitsAvailable = self.__BitsAvailableInLastByte()
        self._numBits += bitsInValue

        if bitsInValue <= bitsAvailable:
            # The value fits in the last byte
            newLastByte = self.__GetLastByte() + (value << (bitsAvailable - bitsInValue))
            self.__SetLastByte(newLastByte)
            return

        bitsLeft = bitsInValue
        if (bitsAvailable > 0):
            # Fill up the last byte
            newLastByte = self.__GetLastByte() + (value >> (bitsInValue - bitsAvailable))
            self.__SetLastByte(newLastByte)
            bitsLeft -= bitsAvailable

        while (bitsLeft >= 8):
            # We have enough bits to fill up an entire byte
            bytenext = ((value >> (bitsLeft - 8)) & 0xFF)
            self.__WriteByte(bytenext)
            bitsLeft -= 8

        if (bitsLeft != 0):
            # Start a new byte with the rest of the bits
            mask = ((1 << bitsLeft) - 1)
            bytenext = ((value & mask) << (8 - bitsLeft))
            self.__WriteByte(bytenext)

    def FindTheFirstZeroBit(self, limit):
        bits = 0
        while (bits < limit):
            bit = self[self._bitPostion]
            self._bitPostion += 1
            if (bit == 0):
                return bits
            bits += 1
        return bits

    def ReadValue(self, bitsToRead):
        if (self._bitPostion + bitsToRead > self._length * 8):
            raise Exception("exceed length")

        value = 0
        for i in range(bitsToRead):
            value <<= 1
            value += self[self._bitPostion]
            self._bitPostion += 1
        return value

    def IsAtEndOfBuffer(self):
        return self._bitPostion >= self._numBits

    def __BitsAvailableInLastByte(self):
        """ return 0~7 """
        bitsAvailable = (8 - (self._numBits & 0x7)) if ((self._numBits & 0x7) != 0) else 0
        return bitsAvailable

    def __GetLastByte(self):
        if self._length == 0:
            return 0
        return self._buffer[self._length - 1]

    def __SetLastByte(self, newValue):
        self.__SetByteAt(self._length - 1, newValue)   

    def __SetByteAt(self, offset, newValue):
        if (self._length == 0):
            self.__WriteByte(newValue)
        else:
            self._buffer[offset] = newValue

    def __WriteByte(self, value):
        if self._length >= self._capacity:
            self.__GrowBuffer()

        self._buffer[self._length] = value
        self._length += 1

    def __GrowBuffer(self):
        newLength = self._capacity * 2
        newBuffer = np.hstack((self._buffer, np.ones(self._capacity, dtype=np.uint8)))
        self._buffer = newBuffer
        self._capacity = newLength

    def __str__(self):
        ret = ""
        for i in range(len(self)):
            ret += str(self[i])
        return ret

    def __len__(self):
        return self._numBits

    def __getitem__(self, i):
        if (i < 0):
            i = self._numBits + i
        return (self._buffer[i >> 3] >> (7 - (i & 0x7))) & 1

def test(_numBits):
    bitsAvailable = (8 - (_numBits & 0x7)) if ((_numBits & 0x7) != 0) else 0
    return bitsAvailable

if __name__ == "__main__":
    a = BitBuffer()
    a.AddValue(7, 3)
    a.AddValue(0,4)
    a.AddValue(31,5)
    b = a.ToBytes()
    print(a)
    pass
