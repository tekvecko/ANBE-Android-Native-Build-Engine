#!/data/data/com.termux/files/usr/bin/python3

import subprocess
import sys
import zipfile
from pathlib import Path


class APKDoctor:

    def __init__(self):
        self.errors = []
        self.warnings = []

    def check(self, apk_path):

        apk = Path(apk_path)

        print("\nANBE APK Doctor")
        print("================")

        if not apk.exists():
            self.error("APK soubor neexistuje")
            return self.report()

        print("[✓] APK soubor nalezen")

        self.check_zip(apk)
        self.check_signature(apk)
        self.check_manifest(apk)
        self.check_abi(apk)

        return self.report()


    def check_zip(self, apk):

        try:
            with zipfile.ZipFile(apk, "r") as z:

                files = z.namelist()

                if "AndroidManifest.xml" in files:
                    print("[✓] AndroidManifest.xml")
                else:
                    self.error("Chybí AndroidManifest.xml")


                dex = [
                    x for x in files
                    if x.endswith(".dex")
                ]

                if dex:
                    print(f"[✓] DEX soubory: {len(dex)}")
                else:
                    self.error("Chybí classes.dex")


        except zipfile.BadZipFile:
            self.error("APK není validní ZIP")


    def check_signature(self, apk):

        try:

            result = subprocess.run(
                [
                    "apksigner",
                    "verify",
                    "--verbose",
                    str(apk)
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("[✓] Podpis APK OK")
            else:
                self.warning(
                    "APK nemá platný podpis"
                )

        except FileNotFoundError:

            self.warning(
                "apksigner není nainstalován"
            )


    def check_manifest(self, apk):

        try:

            result = subprocess.run(
                [
                    "aapt",
                    "dump",
                    "badging",
                    str(apk)
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                lines = result.stdout.splitlines()

                for line in lines:

                    if line.startswith("package:"):
                        print("[✓]", line)

                    if "sdkVersion" in line:
                        print("[✓]", line)

            else:
                self.warning(
                    "Manifest nelze přečíst přes aapt"
                )

        except FileNotFoundError:

            self.warning(
                "aapt není dostupný"
            )


    def check_abi(self, apk):

        try:

            with zipfile.ZipFile(apk) as z:

                abis = set()

                for f in z.namelist():

                    if f.startswith("lib/"):

                        parts = f.split("/")

                        if len(parts) > 1:
                            abis.add(parts[1])


                if abis:

                    print(
                        "[✓] ABI:",
                        ", ".join(sorted(abis))
                    )

                else:

                    print(
                        "[i] APK neobsahuje nativní knihovny"
                    )

        except Exception:
            pass


    def error(self, msg):

        print("[✗]", msg)
        self.errors.append(msg)


    def warning(self, msg):

        print("[!]", msg)
        self.warnings.append(msg)


    def report(self):

        print("\n--- REPORT ---")

        if self.errors:
            print("Chyby:")
            for e in self.errors:
                print(" -", e)

        if self.warnings:
            print("Varování:")
            for w in self.warnings:
                print(" -", w)

        if not self.errors:
            print("APK základní kontrolou prošlo")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print(
            "Použití: python apkdoctor.py soubor.apk"
        )
        sys.exit(1)

    APKDoctor().check(sys.argv[1])
