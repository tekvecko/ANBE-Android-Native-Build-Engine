#!/usr/bin/env python3


from pathlib import Path
import shutil



class ResourceRepair:



    def repair(self,ctx):


        root=Path(
            ctx.project
        )



        icon=root/"assets/icon.png"



        if not icon.exists():


            return ctx



        res=root/"android/app/src/main/res"



        res.mkdir(
            parents=True,
            exist_ok=True
        )



        target=res/"icon.png"



        if not target.exists():


            shutil.copy(
                icon,
                target
            )


            ctx.log(
                "[✓] Android icon restored"
            )



        return ctx

