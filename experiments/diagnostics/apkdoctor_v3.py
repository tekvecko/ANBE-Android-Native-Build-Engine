#!/data/data/com.termux/files/usr/bin/python3

import sys
import subprocess
from pathlib import Path


class APKDoctorV3:


    def run(self, apk):

        apk = Path(apk)

        print("""
================================
 ANBE APK Doctor v3
 Full APK Diagnostic Pipeline
================================
""")


        if not apk.exists():

            print("[✗] APK nenalezeno")
            return


        print("[✓] APK:", apk)


        self.run_module(
            "offlinecheck.py",
            apk
        )


        self.run_module(
            "apkdoctor_v2.py",
            apk
        )


        self.install_check(
            apk
        )


        print("""
================================
 ANBE REPORT COMPLETE
================================
""")


    def run_module(self, module, apk):

        path = Path(
            "anbe"
        ) / module


        if path.exists():

            print(
                "\n>>>",
                module
            )

            subprocess.run(
                [
                    sys.executable,
                    str(path),
                    str(apk)
                ]
            )

        else:

            print(
                "[!] Modul chybí:",
                module
            )



    def install_check(self, apk):

        print(
            "\n>>> installcheck.py"
        )


        try:

            subprocess.run(
                [
                    sys.executable,
                    "anbe/installcheck.py",
                    str(apk)
                ]
            )


        except Exception as e:

            print(
                "[!] Install check error:",
                e
            )



if __name__ == "__main__":


    if len(sys.argv) < 2:

        print(
            "Použití:"
            " python anbe/apkdoctor_v3.py aplikace.apk"
        )

        sys.exit(1)


    APKDoctorV3().run(
        sys.argv[1]
    )
