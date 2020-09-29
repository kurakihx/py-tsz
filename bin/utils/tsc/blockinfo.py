from bin.utils.tsc.constants import Constants
class BlockInfo(object):
    def __init__(self, leadingZeros, trailingZeros):
        self.LeadingZeros = leadingZeros
        self.TrailingZeros = trailingZeros
        self.BlockSize = 64 - leadingZeros - trailingZeros

    @classmethod
    def CalulcateBlockInfo(cls, inputv):
        trailingZeros = 64
        mask = 1
        for i in range(64):
            mask <<= 1
            if (inputv & mask) != 0:
                trailingZeros = i
                break

        leadingZeros = cls.CountLeadingZeros64(inputv)

        if (leadingZeros > Constants.MaxLeadingZerosLength):
            leadingZeros = Constants.MaxLeadingZerosLength

        return BlockInfo(leadingZeros, trailingZeros)


    @classmethod
    def CountLeadingZeros64(cls, intx):
        if (intx >= (1 << 32)):
            # There is a non-zero in the upper 32 bits just count that DWORD
            return cls.CountLeadingZeros32(intx >> 32)

        # The whole upper DWORD was zero so count the lower 
        # DWORD plus the 32 bits from the upper.
        return 32 + cls.CountLeadingZeros32((intx & 0xffff_ffff))

    @classmethod
    def CountLeadingZeros32(cls, intx):
        if (intx >= (1 << 16)):
            if (intx >= (1 << 24)):
                n = 24
            else:
                n = 16
        else:
            if (intx >= (1 << 8)):
                n = 8
            else:
                n = 0
        return cls.countLeadingZeros32Lookup[intx >> n] - n

    countLeadingZeros32Lookup = [
            32, 31, 30, 30, 29, 29, 29, 29,
            28, 28, 28, 28, 28, 28, 28, 28,
            27, 27, 27, 27, 27, 27, 27, 27,
            27, 27, 27, 27, 27, 27, 27, 27,
            26, 26, 26, 26, 26, 26, 26, 26,
            26, 26, 26, 26, 26, 26, 26, 26,
            26, 26, 26, 26, 26, 26, 26, 26,
            26, 26, 26, 26, 26, 26, 26, 26,
            25, 25, 25, 25, 25, 25, 25, 25,
            25, 25, 25, 25, 25, 25, 25, 25,
            25, 25, 25, 25, 25, 25, 25, 25,
            25, 25, 25, 25, 25, 25, 25, 25,
            25, 25, 25, 25, 25, 25, 25, 25,
            25, 25, 25, 25, 25, 25, 25, 25,
            25, 25, 25, 25, 25, 25, 25, 25,
            25, 25, 25, 25, 25, 25, 25, 25,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24,
            24, 24, 24, 24, 24, 24, 24, 24
    ]

if __name__ == "__main__":
    BlockInfo.CalulcateBlockInfo(5)