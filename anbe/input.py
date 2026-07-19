#!/usr/bin/env python3

from pathlib import Path
import shutil
import zipfile
import tempfile


class InputResolver:


    def resolve(self, source):


        src=Path(
            source
        ).expanduser().resolve()



        if src.is_dir():

            return src



        if src.is_file():


            if src.suffix.lower()==".zip":


                return self.extract_zip(
                    src
                )



        raise RuntimeError(
            "Unsupported input: "
            +
            str(source)
        )



    def extract_zip(self,archive):


        base=Path(
            tempfile.mkdtemp(
                prefix="anbe-"
            )
        )


        with zipfile.ZipFile(
            archive,
            "r"
        ) as z:

            z.extractall(
                base
            )


        items=list(
            base.iterdir()
        )


        if len(items)==1 and items[0].is_dir():

            return items[0]


        return base

