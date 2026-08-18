#!/data/data/com.termux/files/usr/bin/python3


import struct


class BinaryReader:


    def __init__(self, data):

        self.data = data
        self.pos = 0



    def read_uint16(self):

        value = struct.unpack_from(
            "<H",
            self.data,
            self.pos
        )[0]

        self.pos += 2

        return value



    def read_uint32(self):

        value = struct.unpack_from(
            "<I",
            self.data,
            self.pos
        )[0]

        self.pos += 4

        return value



    def read_bytes(self, size):

        value = self.data[
            self.pos:
            self.pos + size
        ]

        self.pos += size

        return value



    def seek(self, pos):

        self.pos = pos



    def tell(self):

        return self.pos

