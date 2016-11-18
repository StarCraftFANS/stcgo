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
    for line_number, line in enumerate(hex_file, 1):
        # check start code ':'
        if not line.startswith(":"):
            raise Exception("Missing start code ':', line %d, in file '%s'" %
                            (line_number, filename))
        try:
            # remove start code and EOL, and convert the line to bytearray
            line = bytearray(binascii.a2b_hex(line.strip(":\x0D\x0A")))
            # check data checksum
            if sum(line) & 0xFF != 0x00:
                raise Exception("Incorrect checksum, line %d, in file '%s'" %
                                (line_number, filename))
            # unpack and check the data format
            record = struct.unpack(">BHB%dsb" % line[0], line)
            (data_size, address, record_type, record_data, checksum) = record
        except:
            raise Exception("Invalid format, line %d, in file '%s'" %
                            (line_number, filename))
        # process record_data
        if record_type == 0:  # record type: Data
            padding = max(0, address + data_size - data_length)
            if padding:
                data += bytearray(padding)
                data_length += padding
            data[address:address + data_size] = record_data
        elif record_type == 1:  # record type: End of File
            break
        else:  # other record types (2, 3, 4, 5) are not for STC 8051
            raise Exception("Record type is not data, line %d, in file '%s'" %
                            (line_number, filename))
    hex_file.close()
    # check the end-of-file is the last record
    if record_type != 0x01 or data_size != 0x00:
        raise Exception("Missing EOF in file '%s'" % (line_number, filename))
    # data is good to go
    return data


if __name__ == '__main__':
    print repr(hex2bin("E:\Git\stcgo\sample\led.hex"))
