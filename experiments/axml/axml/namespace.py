#!/data/data/com.termux/files/usr/bin/python3


class NamespaceResolver:


    ANDROID_URI = (
        "http://schemas.android.com/apk/res/android"
    )



    def __init__(self):

        self.namespaces = {}



    def add(self, prefix, uri):

        self.namespaces[prefix] = uri



    def resolve(self, name, uri=None):


        if uri == self.ANDROID_URI:

            return "android:" + str(name)


        return name

