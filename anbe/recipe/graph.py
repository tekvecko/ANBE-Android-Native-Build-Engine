#!/usr/bin/env python3

from .step import RecipeStep


class RecipeGraph:

    @classmethod
    def normalize(
        cls,
        steps
    ):

        return RecipeStep.normalize_all(
            steps
        )


    @classmethod
    def validate(
        cls,
        steps
    ):

        steps = cls.normalize(
            steps
        )

        errors = []

        ids = [
            step["id"]
            for step in steps
        ]

        if len(ids) != len(set(ids)):

            duplicates = sorted({
                step_id
                for step_id in ids
                if ids.count(step_id) > 1
            })

            errors.append(
                "duplicate step ids: "
                +
                ", ".join(duplicates)
            )

        known = set(
            ids
        )

        for step in steps:

            step_id = step[
                "id"
            ]

            for dependency in step.get(
                "depends_on",
                []
            ):

                if dependency == step_id:

                    errors.append(
                        f"step {step_id} depends on itself"
                    )

                elif dependency not in known:

                    errors.append(
                        f"step {step_id} depends on missing step "
                        f"{dependency}"
                    )

        if errors:
            return errors

        try:

            cls.topological_sort(
                steps
            )

        except ValueError as exc:

            errors.append(
                str(exc)
            )

        return errors


    @classmethod
    def assert_valid(
        cls,
        steps
    ):

        errors = cls.validate(
            steps
        )

        if errors:

            raise ValueError(
                "Invalid recipe dependency graph: "
                +
                "; ".join(errors)
            )

        return True


    @classmethod
    def topological_sort(
        cls,
        steps
    ):

        steps = cls.normalize(
            steps
        )

        by_id = {
            step["id"]:
            step
            for step in steps
        }

        order_index = {
            step["id"]:
            index
            for index, step in enumerate(
                steps
            )
        }

        indegree = {
            step_id: 0
            for step_id in by_id
        }

        children = {
            step_id: []
            for step_id in by_id
        }

        for step in steps:

            for dependency in step.get(
                "depends_on",
                []
            ):

                if dependency not in by_id:

                    raise ValueError(
                        f"step {step['id']} depends on missing step "
                        f"{dependency}"
                    )

                indegree[
                    step["id"]
                ] += 1

                children[
                    dependency
                ].append(
                    step["id"]
                )

        ready = [
            step["id"]
            for step in steps
            if indegree[
                step["id"]
            ] == 0
        ]

        result = []

        while ready:

            ready.sort(
                key=lambda step_id:
                order_index[step_id]
            )

            current = ready.pop(
                0
            )

            result.append(
                by_id[current]
            )

            for child in children[
                current
            ]:

                indegree[
                    child
                ] -= 1

                if indegree[
                    child
                ] == 0:

                    ready.append(
                        child
                    )

        if len(result) != len(steps):

            blocked = [
                step_id
                for step_id, value
                in indegree.items()
                if value > 0
            ]

            raise ValueError(
                "dependency cycle detected: "
                +
                ", ".join(
                    sorted(blocked)
                )
            )

        return result
