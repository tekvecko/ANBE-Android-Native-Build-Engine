#!/usr/bin/env python3

from zipfile import ZipFile
from .axml.parser import AXMLParser


class ManifestAnalyzer:

    def analyze(self, apk_path):

        result = {
            "package": None,
            "activities": [],
            "permissions": set(),
            "sdk": {
                "min": None,
                "target": None
            }
        }

        with ZipFile(apk_path) as z:
            data = z.read("AndroidManifest.xml")

        parser = AXMLParser(data)

        for event in parser.parse():

            tag = event.get("tag")
            attrs = event.get("attributes", [])

            if tag == "uses-permission":
                for a in attrs:
                    if a["name"] == "name":
                        result["permissions"].add(
                            a["value"]
                        )

            elif tag == "activity":

                for a in attrs:
                    if a["name"] == "name":
                        result["activities"].append(
                            a["value"]
                        )

            elif tag == "manifest":

                for a in attrs:
                    if a["name"] == "package":
                        result["package"] = a["value"]

            elif tag == "uses-sdk":

                for a in attrs:

                    if a["name"] == "minSdkVersion":

                        typed = a.get("typed")

                        if result["sdk"]["min"] is None:
                            if isinstance(typed, int):
                                result["sdk"]["min"] = typed
                            elif isinstance(a.get("value"), int):
                                result["sdk"]["min"] = a["value"]


                    if a["name"] == "targetSdkVersion":

                        typed = a.get("typed")

                        if result["sdk"]["target"] is None:
                            if isinstance(typed, int):
                                result["sdk"]["target"] = typed
                            elif isinstance(a.get("value"), int):
                                result["sdk"]["target"] = a["value"]

                        else:
                            result["sdk"]["target"] = typed

        result["permissions"] = sorted(
            result["permissions"]
        )

        return result
