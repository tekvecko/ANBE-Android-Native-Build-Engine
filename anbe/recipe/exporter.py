#!/usr/bin/env python3


from pathlib import Path
import json
from datetime import datetime



class RecipeExporter:



    def save(self,ctx):


        out=Path(
            "reports"
        )


        out.mkdir(
            exist_ok=True
        )


        file=out/(
            "recipe-generated-"
            +
            datetime.now()
            .strftime("%Y%m%d-%H%M%S")
            +
            ".json"
        )



        file.write_text(

            json.dumps(

                ctx.recipe,

                indent=2

            )

        )


        ctx.log(
            "[✓] Recipe exported: "
            +
            str(file)
        )


        return ctx

