#!/data/data/com.termux/files/usr/bin/python3

from .contract import ContextContract, ContractError



class ContextValidator:


    def check(self, ctx, stage):


        try:

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


