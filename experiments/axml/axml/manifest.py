#!/data/data/com.termux/files/usr/bin/python3

import zipfile
from pathlib import Path

from .parser import AXMLParser


class ManifestAnalyzer:


    def __init__(self, apk):

        self.apk = Path(apk)

        self.result = {

            "package": None,

            "versionName": None,

            "versionCode": None,

            "sdk": {

                "min": None,

                "target": None

            },

            "permissions": [],

            "activities": [],

            "services": [],

            "receivers": [],

            "providers": []

        }



    def analyze(self):

        data = self.extract()


        if not data:

            return self.result



        parser = AXMLParser(data)


        events = parser.parse()



        for e in events:


            if e["type"] != "start":

                continue



            tag = e.get("tag")

            attrs = self.attrs(
                e.get("attributes", [])
            )



            if tag == "manifest":

                self.result["package"] = attrs.get(
                    "package"
                )

                self.result["versionName"] = attrs.get(
                    "versionName"
                )

                self.result["versionCode"] = attrs.get(
                    "versionCode"
                )



            elif tag == "uses-sdk":

                self.result["sdk"]["min"] = attrs.get(
                    "minSdkVersion"
                )

                self.result["sdk"]["target"] = attrs.get(
                    "targetSdkVersion"
                )



            elif tag == "uses-permission":

                name = (

                    attrs.get("name")

                    or

                    attrs.get("android:name")

                )


                if name:

                    self.result["permissions"].append(
                        name
                    )



            elif tag == "activity":

                self.result["activities"].append(
                    attrs
                )



            elif tag == "service":

                self.result["services"].append(
                    attrs
                )



            elif tag == "receiver":

                self.result["receivers"].append(
                    attrs
                )



            elif tag == "provider":

                self.result["providers"].append(
                    attrs
                )



        return self.result



    def attrs(self, items):

        out = {}

        for item in items:

            name = item.get(
                "name"
            )

            value = item.get(
                "value"
            )


            if not name:

                continue


            if item.get("namespace"):

                if item["namespace"].endswith(
                    "/android"
                ):

                    name = (
                        "android:"
                        + name
                    )


            out[name] = value


        return out



    def extract(self):

        try:

            with zipfile.ZipFile(
                self.apk
            ) as z:

                return z.read(
                    "AndroidManifest.xml"
                )


        except Exception:

            print(
                "[✗] Manifest read failed"
            )

            return None

