#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import struct
import binascii


def hex2bin(filename):
    """Read an Intel HEX file, convert the hex data to binary data, and return
    the data as a bytearray"""
    # open the file
    try:
        hex_file = open(filename, "r")
    except:
        print "Failed to open file '%s'" % filename
        sys.exit(1)
    # transform the data
    data = bytearray()
    data_length = 0
    # data_base = 0x00  # no use for STC 8051
    for line_number, line in enumerate(hex_file):
        # check start code ':'
        if not line.startswith(":"):
            raise Exception("Missing start code ':', line %d, in file '%s'" %
                            (line_number + 1, filename))
        # remove start code and EOL, and convert it to bytearray
        # then unpack the data and check the data format
        try:
            barray = bytearray(binascii.a2b_hex(line.strip(":\x0D\x0A")))
            data_format = ">BHB%dsb" % barray[0]
            record = struct.unpack(data_format, barray)
            (byte_count, offset, record_type, record_data, checksum) = record
        except:
            raise Exception("Invalid format, line %d, in file '%s'" %
                            (line_number + 1, filename))
        # check data checksum
        if sum(barray) & 0xFF:
            raise Exception("Incorrect checksum, line %d, in file '%s'" %
                            (line_number + 1, filename))
        # process record_data
        if record_type == 0:  # record type: Data
            padding = max(0, offset + byte_count - data_length)
            data_length += padding
            data += bytearray(padding)
            data[offset:offset + byte_count] = record_data
        elif record_type == 1:  # record type: End of File
            break
        else:  # other record types (2, 3, 4, 5) are not for STC 8051
            raise Exception("Record type is not data, line %d, in file '%s'" %
                            (line_number + 1, filename))
    hex_file.close()
    # check if the last record is the End of File
    if record_type != 1 or byte_count != 0:
        raise Exception("Missing EOF in file '%s'" %
                        (line_number + 1, filename))
    else:
        return data


if __name__ == '__main__':
    print repr(hex2bin("sample/led.hex"))
