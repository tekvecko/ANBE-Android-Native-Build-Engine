#!/data/data/com.termux/files/usr/bin/python3

import sys
import zipfile
import hashlib
import subprocess
from pathlib import Path


class APKDoctor:

    def __init__(self):
        self.errors = []
        self.warn = []

    def run(self, apk):

        apk = Path(apk)

        print("""
ANBE APK Doctor v2
==================
""")

        if not apk.exists():
            self.fail("APK neexistuje")
            return

        self.info("Soubor nalezen")

        self.hash(apk)
        self.zip_check(apk)
        self.dex_check(apk)
        self.lib_check(apk)
        self.tool_check(apk)

        self.report()


    def zip_check(self, apk):

        try:
            with zipfile.ZipFile(apk) as z:

                files = z.namelist()

                if "AndroidManifest.xml" in files:
                    self.ok("Manifest")

                else:
                    self.fail("Chybí AndroidManifest.xml")


        except Exception:
            self.fail("APK je poškozené")


    def dex_check(self, apk):

        with zipfile.ZipFile(apk) as z:

            dex = [
                x for x in z.namelist()
                if x.endswith(".dex")
            ]

            if dex:
                self.ok(
                    "DEX počet: " + str(len(dex))
                )
            else:
                self.fail("Žádný DEX")


    def lib_check(self, apk):

        with zipfile.ZipFile(apk) as z:

            libs = [
                x for x in z.namelist()
                if x.startswith("lib/")
            ]

            if libs:

                abis = set()

                for l in libs:
                    p=l.split("/")

                    if len(p)>1:
                        abis.add(p[1])

                self.info(
                    "ABI: " +
                    ",".join(sorted(abis))
                )

            else:

                self.info(
                    "Bez nativních knihoven"
                )


    def hash(self, apk):

        h=hashlib.sha256()

        with open(apk,"rb") as f:

            for block in iter(
                lambda:f.read(65536),
                b""
            ):
                h.update(block)

        self.info(
            "SHA256: " + h.hexdigest()
        )


    def tool_check(self, apk):

        tools=[
            "apksigner",
            "aapt",
            "adb"
        ]

        for t in tools:

            try:

                r=subprocess.run(
                    [t,"version"],
                    capture_output=True
                )

                if r.returncode==0:
                    self.ok(t)

                else:
                    self.warn.append(
                        t+" nedostupný"
                    )

            except FileNotFoundError:

                self.warn.append(
                    t+" není nainstalován"
                )


    def ok(self,x):
        print("[✓]",x)


    def info(self,x):
        print("[i]",x)


    def fail(self,x):
        print("[✗]",x)
        self.errors.append(x)


    def report(self):

        print("\n--- REPORT ---")

        if self.errors:

            print("Chyby:")

            for e in self.errors:
                print("-",e)

        if self.warn:

            print("Varování:")

            for w in self.warn:
                print("-",w)

        if not self.errors:

            print("APK struktura OK")


if __name__=="__main__":

    if len(sys.argv)<2:

        print(
            "Použití: python apkdoctor_v2.py soubor.apk"
        )
        exit(1)

    APKDoctor().run(sys.argv[1])
