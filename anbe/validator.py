#!/data/data/com.termux/files/usr/bin/python3

from .contract import ContextContract, ContractError
from .core.context_schema import ContextSchema



class ContextValidator:


    def check(self, ctx, stage):


        try:

            ContextSchema.assert_valid(
                ctx
            )


            ContextContract.validate(
                ctx,
                stage
            )


            print(
                "[✓] Contract OK:",
                stage
            )


            return True



        except ContractError as e:


            print()

            print(
                "[X]",
                str(e)
            )

            raise


