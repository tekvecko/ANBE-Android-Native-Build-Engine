#!/usr/bin/env python3

from .recipe.graph import RecipeGraph


class ExecutionPlanner:

    SCHEMA = "anbe.execution.plan.v1"


    def waves(
        self,
        steps
    ):

        steps = RecipeGraph.normalize(
            steps
        )

        RecipeGraph.assert_valid(
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
            for index, step
            in enumerate(steps)
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

        waves = []

        processed = 0

        while ready:

            ready.sort(
                key=lambda step_id:
                order_index[step_id]
            )

            current_wave = list(
                ready
            )

            ready = []

            waves.append(
                current_wave
            )

            for current in current_wave:

                processed += 1

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

        if processed != len(steps):

            raise ValueError(
                "Cannot create execution plan: "
                "dependency graph contains a cycle"
            )

        return waves


    def parallel_safe(
        self,
        step
    ):

        # v1.8 only identifies candidates.
        # It does NOT execute them concurrently.
        #
        # Android preparation and Gradle are explicitly
        # treated as exclusive operations.
        return (
            step.get("type")
            ==
            "command"
        )


    def plan(
        self,
        steps
    ):

        steps = RecipeGraph.normalize(
            steps
        )

        RecipeGraph.assert_valid(
            steps
        )

        by_id = {
            step["id"]:
            step
            for step in steps
        }

        waves = self.waves(
            steps
        )

        wave_data = []

        flattened = []

        for index, wave in enumerate(
            waves,
            1
        ):

            items = [
                by_id[
                    step_id
                ]
                for step_id in wave
            ]

            flattened.extend(
                wave
            )

            parallel_candidates = [
                step["id"]
                for step in items
                if self.parallel_safe(
                    step
                )
            ]

            wave_data.append({
                "index":
                index,

                "steps":
                list(wave),

                "parallel_candidates":
                parallel_candidates,

                "parallelizable":
                (
                    len(items) > 1
                    and
                    len(
                        parallel_candidates
                    )
                    ==
                    len(items)
                ),
            })

        return {
            "schema":
            self.SCHEMA,

            "waves":
            wave_data,

            "order":
            flattened,

            "step_count":
            len(steps),

            "wave_count":
            len(waves),
        }


    def ordered_steps(
        self,
        steps
    ):

        normalized = (
            RecipeGraph.normalize(
                steps
            )
        )

        plan = self.plan(
            normalized
        )

        by_id = {
            step["id"]:
            step
            for step in normalized
        }

        return [
            by_id[
                step_id
            ]
            for step_id
            in plan["order"]
        ]
