#!/data/data/com.termux/files/usr/bin/python3

import json
from pathlib import Path
from datetime import datetime


class ANBEReport:

    def __init__(self):
        self.data = {
            "engine": "ANBE APK Doctor",
            "version": "3.1",
            "time": str(datetime.now()),
            "checks": {}
        }


    def add(self, key, value):

        self.data["checks"][key] = value


    def status(self):

        errors = []

        for k,v in self.data["checks"].items():

            if isinstance(v, dict):

                if v.get("status") == "error":
                    errors.append(k)


        if errors:
            self.data["status"] = "NEEDS_REVIEW"

        else:
            self.data["status"] = "CLEAN"



    def save(self, name="apk_report.json"):

        self.status()

        folder = Path("reports")

        folder.mkdir(
            exist_ok=True
        )

        out = folder / name


        with open(
            out,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.data,
                f,
                indent=4,
                ensure_ascii=False
            )


        print(
            "[✓] Report:",
            out
        )


