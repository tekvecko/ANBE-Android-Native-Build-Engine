#!/data/data/com.termux/files/usr/bin/python3

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(ROOT)
)

import json

from anbe.axml.manifest import ManifestAnalyzer
from anbe.report_engine import ReportEngine


class ManifestReport:


    def __init__(self, apk):

        self.apk = apk



    def run(self):

        print("[*] Reading AndroidManifest.xml")


        manifest = ManifestAnalyzer(
            self.apk
        ).analyze()


        report = ReportEngine(
            self.apk
        )


        report.add_check(
            "manifest",
            "PASS",
            manifest
        )


        if manifest.get("package"):

            report.add_check(
                "package",
                "PASS",
                {
                    "name":
                    manifest["package"]
                }
            )

        else:

            report.warning(
                "package not detected"
            )


        if manifest["sdk"]["min"] or manifest["sdk"]["target"]:

            report.add_check(
                "sdk",
                "PASS",
                manifest["sdk"]
            )

        else:

            report.warning(
                "sdk information missing"
            )


        report.save()


        return manifest



if __name__ == "__main__":

    if len(sys.argv) < 2:

        print(
            "Použití: python anbe/manifest_report.py app.apk"
        )

        sys.exit(1)


    result = ManifestReport(
        sys.argv[1]
    ).run()


    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )
