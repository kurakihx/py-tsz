class Constants(object):
    BlockSizeAdjustment = 1
    BlockSizeLengthBits = 6
    LeadingZerosLengthBits = 5
    MaxLeadingZerosLength = (1 << LeadingZerosLengthBits) - 1


    BitsForFirstTimestamp = 47   # Works until 2038.
    DefaultDelta = 60