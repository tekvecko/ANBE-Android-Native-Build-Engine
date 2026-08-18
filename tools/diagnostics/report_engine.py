#!/data/data/com.termux/files/usr/bin/python3

import json
from pathlib import Path
from datetime import datetime


class ReportEngine:


    def __init__(self, apk):

        self.data = {

            "engine": "ANBE APK Doctor",

            "version": "3.2",

            "time": str(datetime.now()),

            "apk": str(apk),

            "checks": {},

            "warnings": [],

            "errors": []

        }



    def add_check(self, name, status, data=None):

        item = {

            "status": status

        }


        if data:

            item.update(data)


        self.data["checks"][name] = item



    def warning(self, text):

        self.data["warnings"].append(text)



    def error(self, text):

        self.data["errors"].append(text)



    def finalize(self):


        if self.data["errors"]:

            self.data["result"] = "ERROR"


        elif self.data["warnings"]:

            self.data["result"] = "WARNING"


        else:

            self.data["result"] = "CLEAN"



    def save(self):


        self.finalize()


        folder = Path("reports")

        folder.mkdir(
            exist_ok=True
        )


        json_file = folder / "apk_report.json"

        txt_file = folder / "apk_report.txt"



        with open(
            json_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )



        with open(
            txt_file,
            "w",
            encoding="utf-8"
        ) as f:


            f.write(
                "ANBE APK REPORT\n"
            )

            f.write(
                "================\n\n"
            )

            f.write(
                "APK: "
                + self.data["apk"]
                + "\n\n"
            )


            for name,check in self.data["checks"].items():

                f.write(
                    name.upper()
                    + ": "
                    + check["status"]
                    + "\n"
                )


            if self.data["warnings"]:

                f.write("\nWarnings:\n")

                for w in self.data["warnings"]:

                    f.write(
                        "- "
                        + w
                        + "\n"
                    )



            if self.data["errors"]:

                f.write("\nErrors:\n")

                for e in self.data["errors"]:

                    f.write(
                        "- "
                        + e
                        + "\n"
                    )


            f.write(
                "\nFINAL: "
                + self.data["result"]
                + "\n"
            )


        print("[✓] JSON:", json_file)
        print("[✓] TXT :", txt_file)

