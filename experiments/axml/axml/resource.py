#!/data/data/com.termux/files/usr/bin/python3


class ResourceMap:


    def __init__(self):

        self.ids = {}



    def add(self, index, value):

        self.ids[index] = value



    def get(self, index):

        return self.ids.get(
            index
        )

