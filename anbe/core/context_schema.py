#!/usr/bin/env python3

from pathlib import Path


class ContextSchema:

    REQUIRED = {
        "path": (str, Path),

        "project": dict,
        "profile": dict,
        "recipe": dict,
        "plan": dict,

        "runtime": dict,
        "workspace": dict,
        "cache": dict,

        "artifacts": list,
        "exports": list,
        "execution": list,

        "meta": dict,
    }

    OPTIONAL = {
        "plugin": object,
        "aapt2": (str, type(None)),
        "gradle": (str, type(None)),
        "npm": (str, type(None)),
    }


    @classmethod
    def validate(cls, ctx):

        errors = []

        for name, expected in cls.REQUIRED.items():

            if not hasattr(ctx, name):

                errors.append(
                    f"Missing context field: {name}"
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
                    f"Invalid context field "
                    f"{name}: "
                    f"{type(value).__name__}"
                )

        for name, expected in cls.OPTIONAL.items():

            if not hasattr(ctx, name):
                continue

            value = getattr(
                ctx,
                name
            )

            if expected is object:
                continue

            if not isinstance(
                value,
                expected
            ):

                errors.append(
                    f"Invalid optional context field "
                    f"{name}: "
                    f"{type(value).__name__}"
                )

        return errors


    @classmethod
    def assert_valid(cls, ctx):

        errors = cls.validate(
            ctx
        )

        if errors:

            raise TypeError(
                "BuildContext contract violation: "
                +
                "; ".join(errors)
            )

        return True
