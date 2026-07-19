#!/usr/bin/env python3


import sys

from .orchestrator import Orchestrator



def main():


    if len(sys.argv)<3:


        print(
            "Usage:"
        )

        print(
            "  anbe build <project>"
        )

        sys.exit(1)



    command=sys.argv[1]


    project=sys.argv[2]



    if command=="build":


        Orchestrator().run(
            project
        )


    else:


        print(
            "Unknown command:",
            command
        )

        sys.exit(1)



if __name__=="__main__":

    main()

