#!/usr/bin/env python3


from pathlib import Path



class GradleDoctor:



    def repair(self,ctx):


        android=Path(
            ctx.project
        )/"android"



        wrapper=android/"gradlew"



        if wrapper.exists():


            wrapper.chmod(
                0o755
            )


            ctx.log(
                "[✓] gradlew permissions fixed"
            )



        else:


            ctx.log(
                "[!] gradlew missing"
            )


            ctx.failed=True



        properties=android/"gradle.properties"



        if properties.exists():


            text=properties.read_text()



            if (
                "org.gradle.jvmargs"
                not in text
            ):


                text += (
                    "\n"
                    "org.gradle.jvmargs="
                    "-Xmx2048m\n"
                )


                properties.write_text(
                    text
                )


                ctx.log(
                    "[✓] Gradle memory configured"
                )



        return ctx

