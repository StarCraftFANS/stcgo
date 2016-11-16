import sys
import struct
import binascii


def hex2bin(filename):
    """Read an Intel HEX file, convert the hex data to binary data, and return
    the data as a bytearray"""

    # open the file
    try:
        i32hex_file = open(filename, "r")
    except:
        print "Failed to open file '%s'" % filename
        sys.exit(1)

    # transform the data
    data = bytearray()
    base_address = 0x00
    for line_number, line in enumerate(i32hex_file):
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
            (byte_count, address, record_type, record_data, checksum) = record
        except:
            raise Exception("Invalid format, line %d, in file '%s'" %
                            (line_number + 1, filename))
        # data checksum
        if sum(barray) & 0xFF:
            raise Exception("Incorrect checksum, line %d, in file '%s'" %
                            (line_number + 1, filename))
        print record

        data += record_data

    i32hex_file.close()
    return data


def hex2bin_old(code):
    buf = bytearray()
    base = 0
    line = 0

    for rec in code.splitlines():
        # Calculate the line number of the current record
        line += 1

        try:
            # bytes(...) is to support python<=2.6
            # bytearray(...) is to support python<=2.7
            n = bytearray(binascii.a2b_hex(bytes(rec[1:3])))[0]
            dat = bytearray(binascii.a2b_hex(bytes(rec[1:n * 2 + 11])))
        except:
            raise Exception("Line %d: Invalid format" % line)

        if rec[0] != ord(":"):
            raise Exception("Line %d: Missing start code \":\"" % line)
        if sum(dat) & 0xFF != 0:
            raise Exception("Line %d: Incorrect checksum" % line)

        if dat[3] == 0:      # Data record
            addr = base + (dat[1] << 8) + dat[2]
            # Allocate memory space and fill it with 0xFF
            buf[len(buf):] = [0xFF] * (addr + n - len(buf))
            # Copy data to the buffer
            buf[addr:addr + n] = dat[4:-1]

        elif dat[3] == 1:    # EOF record
            if n != 0:
                raise Exception("Line %d: Incorrect data length" % line)

        elif dat[3] == 2:    # Extended segment address record
            if n != 2:
                raise Exception("Line %d: Incorrect data length" % line)
            base = ((dat[4] << 8) + dat[5]) << 4

        elif dat[3] == 4:    # Extended linear address record
            if n != 2:
                raise Exception("Line %d: Incorrect data length" % line)
            base = ((dat[4] << 8) + dat[5]) << 16

        else:
            raise Exception("Line %d: Unsupported record type" % line)

    return buf


if __name__ == '__main__':
    filename = "test/led.hex"
    x1 = hex2bin(filename)
    for c in x1:
        print "%02X " % c,

    print "\n" + "-" * 74
    with open(filename, "rb") as test:
        x2 = hex2bin_old(bytearray(test.read()))
        for c in x2:
            print "%02X " % c,
    print
    print x1 == x2
