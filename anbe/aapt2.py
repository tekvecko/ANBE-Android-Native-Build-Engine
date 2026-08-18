from pathlib import Path


class AAPT2Manager:

    def apply(self, ctx):

        runtime_candidates = [
            Path.home() / "ANBE-Runtime-Pack-v0.1" / "bin" / "aapt2",
            Path("/usr/local/bin/aapt2"),
            Path("/data/data/com.termux/files/usr/bin/aapt2"),
        ]

        aapt2 = None

        for candidate in runtime_candidates:
            if candidate.exists() and candidate.is_file():
                aapt2 = candidate
                break

        if not aapt2:
            raise RuntimeError(
                "AAPT2 executable not found"
            )

        aapt2 = aapt2.resolve()

        gradle_props = Path(ctx.path) / "gradle.properties"

        if gradle_props.exists():

            lines = gradle_props.read_text().splitlines()

            updated = False
            output = []

            for line in lines:
                if line.startswith(
                    "android.aapt2FromMavenOverride="
                ):
                    output.append(
                        f"android.aapt2FromMavenOverride={aapt2}"
                    )
                    updated = True
                else:
                    output.append(line)

            if not updated:
                output.append(
                    f"android.aapt2FromMavenOverride={aapt2}"
                )

            gradle_props.write_text(
                "\n".join(output) + "\n"
            )

        ctx.aapt2 = str(aapt2)

        ctx.runtime["aapt2"] = str(aapt2)

        print(
            f"[✓] AAPT2 override applied: {aapt2}"
        )
