#!/data/data/com.termux/files/usr/bin/python3


class Registry:


    def __init__(self):

        self.items = []


    def register(self, stage):

        self.items.append(stage)


    def __iter__(self):

        return iter(self.items)

