#!/data/data/com.termux/files/usr/bin/python3

from pathlib import Path


class ContractError(Exception):
    pass



class ContextContract:


    REQUIRED = {

        "path": Path,

        "project": dict,

        "runtime": dict,

        "profile": dict,

        "recipe": dict,

        "plan": dict,

        "workspace": dict,

        "artifacts": list,

        "exports": list

    }



    @classmethod
    def validate(cls, ctx, stage="unknown"):

        errors = []


        for name, expected in cls.REQUIRED.items():


            if not hasattr(ctx, name):

                errors.append(

                    f"{name}: missing"

                )

                continue



            value = getattr(
                ctx,
                name
            )


            if not isinstance(
                value,
                expected
            ):

                errors.append(

                    f"{name}: expected "
                    f"{expected.__name__}, "
                    f"got {type(value).__name__}"

                )



        if errors:

            raise ContractError(

                "\n".join([

                    f"ANBE Contract violation",
                    f"Stage: {stage}",
                    "",
                    *errors

                ])

            )


        return True



    @classmethod
    def snapshot(cls, ctx):

        data = {}


        for name in cls.REQUIRED:

            value = getattr(
                ctx,
                name,
                None
            )


            data[name] = type(
                value
            ).__name__


        return data

