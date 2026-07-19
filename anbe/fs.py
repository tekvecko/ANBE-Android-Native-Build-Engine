#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


class FS:


    @staticmethod
    def mkdir(path):

        Path(path).mkdir(

            parents=True,

            exist_ok=True

        )


    @staticmethod
    def exists(path):

        return Path(path).exists()


    @staticmethod
    def read(path):

        return Path(path).read_text()


    @staticmethod
    def write(

        path,

        text

    ):

        Path(path).write_text(text)


    @staticmethod
    def copy(src,dst):

        import shutil

        shutil.copy2(

            src,

            dst

        )

