#!/data/data/com.termux/files/usr/bin/python3

import struct

from .strings import StringPool
from .value import TypedValue
from .locator import AXMLLocator


RES_XML_START_ELEMENT_TYPE = 0x0102
RES_XML_END_ELEMENT_TYPE   = 0x0103


class AXMLParser:


    def __init__(self, data):

        self.data = data
        self.strings = []
        self.events = []



    def parse(self):

        xml_type = struct.unpack_from(
            "<H",
            self.data,
            0
        )[0]


        if xml_type != 0x0003:

            raise ValueError(
                "Not Android XML"
            )


        self.parse_chunks()

        return self.events



    def parse_chunks(self):

        pos = 8


        while pos < len(self.data):

            chunk_type = struct.unpack_from(
                "<H",
                self.data,
                pos
            )[0]


            chunk_size = struct.unpack_from(
                "<I",
                self.data,
                pos + 4
            )[0]


            if chunk_type == 0x0001:

                pool = StringPool(
                    self.data
                )

                self.strings = pool.parse(
                    pos
                )

                self.locator = AXMLLocator(
                    self.data,
                    self.strings
                )


            elif chunk_type == RES_XML_START_ELEMENT_TYPE:

                self.read_start_tag(
                    pos
                )


            elif chunk_type == RES_XML_END_ELEMENT_TYPE:

                self.read_end_tag(
                    pos
                )


            pos += chunk_size



    def get_string(self, index):

        if index == 0xffffffff:

            return None


        if index < len(self.strings):

            return self.strings[index]


        return None



    def read_start_tag(self, pos):


        name_idx = struct.unpack_from(
            "<I",
            self.data,
            pos + 20
        )[0]


        tag = self.get_string(
            name_idx & 0x00ffffff
        )

        print("TAG DEBUG:", name_idx, tag)



        attribute_start = struct.unpack_from(
            "<H",
            self.data,
            pos + 24
        )[0]

        attr_start, attr_count = self.locator.find_attributes(pos)

        attr_size = struct.unpack_from(
            "<H",
            self.data,
            attr_start + 2
        )[0]

        attr_count = struct.unpack_from(
            "<H",
            self.data,
            attr_start + 4
        )[0]

        print(
            "DYNAMIC ATTR:",
            "base=", hex(pos),
            "attr_start=", hex(attr_start),
            "size=", attr_size,
            "count=", attr_count
        )


        attribute_start = struct.unpack_from(
            "<H",
            self.data,
            attr_start
        )[0]


        attr_size = struct.unpack_from(
            "<H",
            self.data,
            attr_start + 2
        )[0]


        attr_count = struct.unpack_from(
            "<H",
            self.data,
            attr_start + 4
        )[0]



        attributes = []


        print("ATTR EXT")
        print("attribute_start =", attribute_start)
        print("attribute_size =", attr_size)
        print("attribute_count =", attr_count)
        print("attr_start hex =", hex(attr_start))
        print(self.data[attr_start-16:attr_start+32].hex(" "))

        offset = attr_start

        for i in range(attr_count):

            ns_idx = struct.unpack_from(
                "<I",
                self.data,
                offset
            )[0]

            name_idx = struct.unpack_from(
                "<I",
                self.data,
                offset + 4
            )[0]

            raw_idx = struct.unpack_from(
                "<I",
                self.data,
                offset + 8
            )[0]

            print(
                "IDX CLEAN",
                "ns", ns_idx & 0x00ffffff,
                "name", name_idx & 0x00ffffff,
                "raw", raw_idx & 0x00ffffff,
                "strings", len(self.strings)
            )

            name = self.get_string(name_idx & 0x00ffffff)

            namespace = None
            if ns_idx != 0xffffffff:
                namespace = self.get_string(ns_idx & 0x00ffffff)

            raw = None
            if raw_idx != 0xffffffff:
                raw = self.get_string(raw_idx & 0x00ffffff)

            print(
                "TYPED BYTES",
                name,
                self.data[offset:offset+32].hex(" ")
            )

            print(
                "TYPED FINAL BYTES",
                self.data[offset:offset+40].hex(" ")
            )

            typed_pos = self.locator.find_typed_value(
                offset
            )

            typed = TypedValue.decode(
                self.data,
                typed_pos,
                self.strings
            )

            value = raw if raw is not None else typed

            if name in ("minSdkVersion", "targetSdkVersion"):
                print(
                    "SDK DEBUG:",
                    name,
                    "typed=",
                    typed,
                    "type=",
                    type(typed),
                    "dict=",
                    getattr(typed, "__dict__", None)
                )

            print(
                "ATTR CHECK:",
                "ns_idx=", ns_idx,
                self.get_string(ns_idx),
                "name_idx=", name_idx,
                self.get_string(name_idx),
                "raw_idx=", raw_idx,
                self.get_string(raw_idx)
            )

            attributes.append(
                {
                    "name": name,
                    "namespace": namespace,
                    "value": value,
                    "typed": getattr(
                        typed,
                        "data",
                        typed
                    )
                }
            )

            offset += attr_size


        self.events.append(
            {
                "type":"start",
                "tag":tag,
                "attributes":attributes
            }
        )



    def read_end_tag(self, pos):


        name_idx = struct.unpack_from(
            "<I",
            self.data,
            pos + 20
        )[0]


        self.events.append(
            {
                "type":"end",
                "tag":self.get_string(
                    name_idx
                )
            }
        )

