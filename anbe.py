#!/data/data/com.termux/files/usr/bin/python


import argparse

from anbe.source import SourceFetcher
from anbe.input import InputResolver
from anbe.builder import Builder



def main():


    parser=argparse.ArgumentParser(
        description="ANBE Universal Android Builder"
    )


    sub=parser.add_subparsers(
        dest="command"
    )


    build=sub.add_parser(
        "build"
    )


    build.add_argument(
        "source"
    )



    args=parser.parse_args()



    if args.command=="build":


        print("="*40)
        print(
            "ANBE Universal Builder v0.3"
        )
        print("="*40)



        source=SourceFetcher().fetch(
            args.source
        )


        project=InputResolver().resolve(
            source
        )



        ctx=Builder().build(
            project
        )



        print()

        if ctx.artifact and ctx.artifact.get(
            "found"
        ):

            print(
                "APK:",
                ctx.artifact["export"]
            )

        else:

            print(
                "APK not produced"
            )



    else:

        parser.print_help()



if __name__=="__main__":

    main()

