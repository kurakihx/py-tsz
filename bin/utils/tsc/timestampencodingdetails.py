class TimestampEncodingDetails(object):
    def __init__(self, bitsForValue, controlValue, controlValueBitLength):
        self.BitsForValue = bitsForValue
        self.ControlValue = controlValue
        self.ControlValueBitLength = controlValueBitLength
        self.MaxValueForEncoding = 1 << (bitsForValue - 1)
    
    Encodings = []
    MaxControlBitLength = 0

TimestampEncodingDetails.Encodings.append(TimestampEncodingDetails(7, 2, 2))
TimestampEncodingDetails.Encodings.append(TimestampEncodingDetails(9, 6, 3))
TimestampEncodingDetails.Encodings.append(TimestampEncodingDetails(12, 14, 4))
TimestampEncodingDetails.Encodings.append(TimestampEncodingDetails(32, 15, 4))
TimestampEncodingDetails.MaxControlBitLength = TimestampEncodingDetails.Encodings[-1].ControlValueBitLength
