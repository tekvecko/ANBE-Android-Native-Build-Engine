#!/data/data/com.termux/files/usr/bin/python3

class Logger:

    def ok(self, text):

        print("[✓]", text)

    def info(self, text):

        print("[>]", text)

    def warn(self, text):

        print("[!]", text)

    def error(self, text):

        print("[X]", text)

