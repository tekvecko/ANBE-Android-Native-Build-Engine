#!/usr/bin/env python3

import struct


def u16(data, p):
    return struct.unpack_from("<H", data, p)[0]


def u32(data, p):
    return struct.unpack_from("<I", data, p)[0]


class AXMLLocator:

    def __init__(self, data, strings):
        self.data = data
        self.strings = strings


    def find_attributes(self, pos):

        size = len(self.data)

        # START_TAG header:
        # chunk + line + comment + ns + name
        base = pos + 16

        # scan possible attribute extension
        for off in range(pos + 20, pos + 64, 4):

            if off + 8 >= size:
                continue

            try:
                attr_start = u16(self.data, off)
                attr_size  = u16(self.data, off + 2)
                attr_count = u16(self.data, off + 4)

            except Exception:
                continue


            if attr_count <= 0 or attr_count > 200:
                continue


            if attr_size not in (20,):
                continue


            attrs = off + attr_start

            if attrs + attr_count * attr_size > size:
                continue


            good = True


            for i in range(attr_count):

                p = attrs + i * attr_size

                name_idx = u32(
                    self.data,
                    p + 4
                ) & 0xffffff


                if name_idx >= len(self.strings):
                    good = False
                    break


            if good:
                return attrs, attr_count


        raise RuntimeError(
            "AXML attributes not found"
        )


    def find_typed_value(self, attr_pos):
        return attr_pos + 12
