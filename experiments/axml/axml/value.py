#!/data/data/com.termux/files/usr/bin/python3

import struct


TYPE_NULL = 0x00
TYPE_REFERENCE = 0x01
TYPE_ATTRIBUTE = 0x02
TYPE_STRING = 0x03
TYPE_FLOAT = 0x04
TYPE_DIMENSION = 0x05
TYPE_FRACTION = 0x06

TYPE_INT_DEC = 0x10
TYPE_INT_HEX = 0x11
TYPE_INT_BOOLEAN = 0x12


class TypedValue:

    @staticmethod
    def decode(data, pos, strings):

        dtype = struct.unpack_from(
            "<B",
            data,
            pos + 3
        )[0]

        # oprava pro některé AXML integer zápisy
        if dtype not in (
            TYPE_NULL,
            TYPE_STRING,
            TYPE_INT_DEC,
            TYPE_INT_HEX,
            TYPE_INT_BOOLEAN,
            TYPE_REFERENCE
        ):
            alt = pos + 8

            if alt + 8 <= len(data):
                dtype = struct.unpack_from(
                    "<B",
                    data,
                    alt + 3
                )[0]

                if dtype in (
                    TYPE_NULL,
                    TYPE_STRING,
                    TYPE_INT_DEC,
                    TYPE_INT_HEX,
                    TYPE_INT_BOOLEAN,
                    TYPE_REFERENCE
                ):
                    pos = alt

        value = struct.unpack_from(
            "<I",
            data,
            pos + 4
        )[0]


        if dtype == TYPE_NULL:

            if value != 0xffffffff:
                return value

            return None


        if dtype == TYPE_STRING:

            if value < len(strings):
                return strings[value]

            return None


        if dtype == TYPE_INT_DEC:
            return value


        if dtype == TYPE_INT_HEX:
            return value


        if dtype == TYPE_INT_BOOLEAN:
            return bool(value)


        if dtype == TYPE_REFERENCE:
            return "@"+hex(value)


        return value
