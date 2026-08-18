#!/usr/bin/env python3

from copy import deepcopy


class RecipeStep:

    SCHEMA = "anbe.recipe.step.v1"

    TYPES = {
        "command",
        "android_prepare",
        "gradle",
    }

    LEGACY = {
        "npm install": {
            "id": "npm-install",
            "type": "command",
            "command": "npm install",
            "cwd": "project",
        },

        "npm run build": {
            "id": "npm-build",
            "type": "command",
            "command": "npm run build",
            "cwd": "project",
        },

        "npx cap sync android": {
            "id": "capacitor-sync-android",
            "type": "command",
            "command": "npx cap sync android",
            "cwd": "project",
        },

        "android prepare": {
            "id": "android-prepare",
            "type": "android_prepare",
            "cwd": "android",
        },

        "gradle assembleDebug": {
            "id": "gradle-assemble-debug",
            "type": "gradle",
            "task": "assembleDebug",
            "cwd": "android",
        },
    }


    @classmethod
    def command(
        cls,
        step_id,
        command,
        cwd="project",
        depends_on=None,
    ):

        return {
            "schema": cls.SCHEMA,
            "id": step_id,
            "type": "command",
            "command": command,
            "cwd": cwd,
            "depends_on": list(
                depends_on or []
            ),
        }


    @classmethod
    def android_prepare(
        cls,
        depends_on=None,
    ):

        return {
            "schema": cls.SCHEMA,
            "id": "android-prepare",
            "type": "android_prepare",
            "cwd": "android",
            "depends_on": list(
                depends_on or []
            ),
        }


    @classmethod
    def gradle(
        cls,
        task="assembleDebug",
        depends_on=None,
    ):

        return {
            "schema": cls.SCHEMA,
            "id": (
                "gradle-"
                +
                task.lower()
            ),
            "type": "gradle",
            "task": task,
            "cwd": "android",
            "depends_on": list(
                depends_on or []
            ),
        }


    @classmethod
    def normalize(
        cls,
        step
    ):

        if isinstance(
            step,
            str
        ):

            mapped = cls.LEGACY.get(
                step
            )

            if mapped is None:

                # Generic legacy shell command.
                return cls.command(
                    "legacy-command",
                    step,
                )

            result = deepcopy(
                mapped
            )

            result[
                "schema"
            ] = cls.SCHEMA

            return result

        if isinstance(
            step,
            dict
        ):

            result = deepcopy(
                step
            )

            result.setdefault(
                "schema",
                cls.SCHEMA
            )

            result.setdefault(
                "depends_on",
                []
            )

            return result

        raise TypeError(
            "Recipe step must be string or dict, got: "
            +
            type(step).__name__
        )


    @classmethod
    def validate(
        cls,
        step
    ):

        errors = []

        if not isinstance(
            step,
            dict
        ):

            return [
                "step is not an object"
            ]

        step_type = step.get(
            "type"
        )

        if step_type not in cls.TYPES:

            errors.append(
                "unsupported step type: "
                +
                str(step_type)
            )

        if not step.get(
            "id"
        ):

            errors.append(
                "missing step id"
            )

        if (
            step_type
            ==
            "command"
            and
            not step.get(
                "command"
            )
        ):

            errors.append(
                "command step missing command"
            )

        if (
            step_type
            ==
            "gradle"
            and
            not step.get(
                "task"
            )
        ):

            errors.append(
                "gradle step missing task"
            )

        depends_on = step.get(
            "depends_on",
            []
        )

        if not isinstance(
            depends_on,
            list
        ):

            errors.append(
                "depends_on must be a list"
            )

        elif not all(
            isinstance(item, str)
            and item
            for item in depends_on
        ):

            errors.append(
                "depends_on entries must be non-empty strings"
            )

        elif len(
            depends_on
        ) != len(
            set(depends_on)
        ):

            errors.append(
                "depends_on contains duplicates"
            )

        cwd = step.get(
            "cwd"
        )

        if cwd not in (
            None,
            "project",
            "android",
        ):

            errors.append(
                "invalid cwd selector: "
                +
                str(cwd)
            )

        return errors


    @classmethod
    def assert_valid(
        cls,
        step
    ):

        errors = cls.validate(
            step
        )

        if errors:

            raise ValueError(
                "Invalid recipe step: "
                +
                "; ".join(
                    errors
                )
            )

        return True


    @classmethod
    def normalize_all(
        cls,
        steps
    ):

        result = []

        for step in steps:

            normalized = cls.normalize(
                step
            )

            cls.assert_valid(
                normalized
            )

            result.append(
                normalized
            )

        return result
