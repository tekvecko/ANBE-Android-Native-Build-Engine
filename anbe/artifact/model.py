#!/usr/bin/env python3


from pathlib import Path



class ArtifactCollector:



    def collect(self,ctx):


        path = ctx.recipe.get(
            "artifact"
        )


        if not path:

            ctx.artifact={

                "found":False

            }

            return ctx



        apk=Path(
            ctx.project
        ) / path



        if apk.exists():


            export=Path(
                "~/storage/downloads/anbe-build.apk"
            ).expanduser()



            export.parent.mkdir(
                parents=True,
                exist_ok=True
            )


            export.write_bytes(
                apk.read_bytes()
            )


            ctx.artifact={

                "found":True,

                "source":
                str(apk),

                "export":
                str(export)

            }


            ctx.log(
                "[✓] APK exported"
            )



        else:


            ctx.artifact={

                "found":False,

                "expected":
                str(apk)

            }



        return ctx

