#!/data/data/com.termux/files/usr/bin/python3

import subprocess
import sys
from pathlib import Path


class InstallChecker:

    def __init__(self):
        self.result = ""

    def run(self, apk):

        apk = Path(apk)

        print("""
ANBE Install Checker
====================
""")

        if not apk.exists():
            print("[✗] APK neexistuje")
            return

        print("[✓] APK nalezeno")

        try:

            proc = subprocess.run(
                [
                    "adb",
                    "install",
                    "-r",
                    str(apk)
                ],
                capture_output=True,
                text=True
            )

            output = (
                proc.stdout +
                "\n" +
                proc.stderr
            )

            self.result = output

            print(output)

            self.analyze(output)


        except FileNotFoundError:

            print(
                "[✗] adb není dostupné"
            )


    def analyze(self, text):

        print("\n--- ANBE DIAGNOSTIKA ---")


        if "no devices/emulators found" in text:

            print("[!] ADB zařízení není připojeno")
            print("    Připoj telefon přes USB debugging")
            print("    nebo:")
            print("    adb connect IP:PORT")

            return


        if "unauthorized" in text:

            print("[!] Zařízení čeká na ADB autorizaci")
            print("    Potvrď RSA dialog v telefonu")

            return


        if "offline" in text:

            print("[!] ADB zařízení je offline")

            return


        checks = [

            (
                "INSTALL_FAILED_NO_MATCHING_ABIS",
                "APK neobsahuje podporovanou architekturu zařízení."
            ),

            (
                "INSTALL_FAILED_VERSION_DOWNGRADE",
                "APK má nižší verzi než nainstalovaná aplikace."
            ),

            (
                "INSTALL_FAILED_UPDATE_INCOMPATIBLE",
                "Podpis APK nesouhlasí s existující aplikací."
            ),

            (
                "INSTALL_PARSE_FAILED_NO_CERTIFICATES",
                "APK není podepsané."
            ),

            (
                "INSTALL_FAILED_INVALID_APK",
                "APK je poškozené."
            ),

            (
                "INSTALL_FAILED_INSUFFICIENT_STORAGE",
                "Nedostatek místa."
            )
        ]


        for code, msg in checks:

            if code in text:

                print("[✗]", code)
                print("   ", msg)
                return


        if "Success" in text:

            print("[✓] Instalace úspěšná")

        else:

            print("[?] Neznámá chyba")
