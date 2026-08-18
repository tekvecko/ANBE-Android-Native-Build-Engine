#!/data/data/com.termux/files/usr/bin/python3

import sys
import zipfile
import hashlib
from pathlib import Path


class OfflineAPKCheck:


    def run(self, apk):

        apk = Path(apk)

        print("""
ANBE Offline APK Analyzer
=========================
""")

        if not apk.exists():

            print("[✗] APK nenalezeno")
            return


        print("[✓] APK nalezeno")

        self.sha256(apk)
        self.structure(apk)

        self.report()



    def sha256(self, apk):

        h = hashlib.sha256()

        with open(apk,"rb") as f:

            for block in iter(
                lambda:f.read(65536),
                b""
            ):
                h.update(block)

        print(
            "[i] SHA256:",
            h.hexdigest()
        )



    def structure(self, apk):

        self.errors = []
        self.warn = []

        try:

            with zipfile.ZipFile(apk) as z:

                files = z.namelist()


                if "AndroidManifest.xml" in files:

                    print("[✓] Manifest")

                else:

                    self.errors.append(
                        "Chybí AndroidManifest.xml"
                    )


                dex = [
                    x for x in files
                    if x.endswith(".dex")
                ]

                if dex:

                    print(
                        "[✓] DEX:",
                        len(dex)
                    )

                else:

                    self.errors.append(
                        "Chybí classes.dex"
                    )


                libs = [
                    x for x in files
                    if x.startswith("lib/")
                ]


                if libs:

                    abi=set()

                    for x in libs:

                        p=x.split("/")

                        if len(p)>1:
                            abi.add(p[1])


                    print(
                        "[i] ABI:",
                        ",".join(sorted(abi))
                    )

                else:

                    print(
                        "[i] Bez nativních knihoven"
                    )


                certs=[
                    x for x in files
                    if x.startswith(
                        "META-INF/"
                    )
                ]


                if certs:

                    print(
                        "[✓] META-INF podpisové soubory"
                    )

                else:

                    self.warn.append(
                        "Nenalezen podpisový blok"
                    )


        except zipfile.BadZipFile:

            self.errors.append(
                "Poškozený ZIP/APK"
            )



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

            print(
                "APK prošlo offline kontrolou"
            )



if __name__=="__main__":

    if len(sys.argv)<2:

        print(
            "Použití:"
            " python offlinecheck.py soubor.apk"
        )

        sys.exit(1)


    OfflineAPKCheck().run(sys.argv[1])
