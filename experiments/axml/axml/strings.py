#!/data/data/com.termux/files/usr/bin/python3


import struct


class StringPool:


    def __init__(self, data):

        self.data = data
        self.strings = []



    def parse(self, offset):

        data = self.data


        # chunk header
        chunk_type = struct.unpack_from(
            "<H",
            data,
            offset
        )[0]


        if chunk_type != 0x0001:

            raise ValueError(
                "Invalid String Pool"
            )


        header_size = struct.unpack_from(
            "<H",
            data,
            offset + 2
        )[0]


        chunk_size = struct.unpack_from(
            "<I",
            data,
            offset + 4
        )[0]


        string_count = struct.unpack_from(
            "<I",
            data,
            offset + 8
        )[0]


        style_count = struct.unpack_from(
            "<I",
            data,
            offset + 12
        )[0]


        flags = struct.unpack_from(
            "<I",
            data,
            offset + 16
        )[0]


        strings_offset = struct.unpack_from(
            "<I",
            data,
            offset + 20
        )[0]


        utf8 = bool(
            flags & 0x100
        )


        offsets = []

        pos = offset + header_size


        for i in range(string_count):

            value = struct.unpack_from(
                "<I",
                data,
                pos
            )[0]

            offsets.append(value)

            pos += 4



        base = offset + strings_offset


        for off in offsets:

            if utf8:

                s = self.read_utf8(
                    base + off
                )

            else:

                s = self.read_utf16(
                    base + off
                )


            self.strings.append(s)



        return self.strings



    def read_utf8(self, pos):

        data = self.data


        length = data[pos + 1]

        start = pos + 2


        raw = b""


        while data[start] != 0:

            raw += bytes(
                [data[start]]
            )

            start += 1


        return raw.decode(
            "utf-8",
            errors="replace"
        )



    def read_utf16(self, pos):

        data = self.data


        length = struct.unpack_from(
            "<H",
            data,
            pos
        )[0]


        pos += 2


        raw = b""


        for i in range(length):

            raw += data[
                pos:
                pos + 2
            ]

            pos += 2


        return raw.decode(
            "utf-16le",
            errors="replace"
        )



    def get(self, index):

        if index < 0:

            return None


        if index >= len(
            self.strings
        ):

            return None


        return self.strings[index]

