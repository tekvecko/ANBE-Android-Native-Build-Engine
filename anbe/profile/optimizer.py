#!/usr/bin/env python3



class ProfileOptimizer:



    def optimize(self,ctx):


        profile=ctx.profile



        if (
            profile.get("environment")
            ==
            "termux"
        ):


            profile["gradle"]={

                "daemon":
                False,

                "parallel":
                False

            }



            profile["aapt2"]="ANBE-runtime"



        if (
            profile.get("artifact")
            ==
            "apk"
        ):


            profile["export"]="downloads"



        ctx.profile=profile



        ctx.log(
            "[✓] Profile optimized"
        )



        return ctx

