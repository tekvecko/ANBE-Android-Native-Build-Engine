#!/usr/bin/env python3


from pathlib import Path



class AndroidCleaner:



    def repair(self,ctx):


        android=Path(
            ctx.project
        )/"android"



        files=[


            android/
            "capacitor-cordova-android-plugins",


        ]



        for item in files:


            if item.exists():


                ctx.log(
                    "[!] Found Cordova leftovers: "
                    +
                    str(item)
                )


        settings=android/"settings.gradle"



        if settings.exists():


            data=settings.read_text()



            if "cordova" in data.lower():


                ctx.log(
                    "[>] Cordova reference detected"
                )



        return ctx

