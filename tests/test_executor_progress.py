#!/usr/bin/env python3

from anbe.executor import Executor


def test_executor_progress_empty():

    executor = Executor()

    assert (
        executor.progress_percent(
            0,
            0,
        )
        ==
        100
    )


def test_executor_progress_two_steps():

    executor = Executor()

    assert (
        executor.progress_percent(
            0,
            2,
        )
        ==
        0
    )

    assert (
        executor.progress_percent(
            1,
            2,
        )
        ==
        50
    )

    assert (
        executor.progress_percent(
            2,
            2,
        )
        ==
        100
    )


def test_executor_progress_five_steps():

    executor = Executor()

    values = [
        executor.progress_percent(
            completed,
            5,
        )
        for completed
        in range(
            0,
            6,
        )
    ]

    assert values == [
        0,
        20,
        40,
        60,
        80,
        100,
    ]
