from pathlib import Path
from tempfile import TemporaryDirectory

from anbe.gradle_compatibility import GradleCompatibility


def project(
    root,
    wrapper_url,
    agp,
):

    root = Path(
        root
    )

    wrapper = (
        root
        /
        "gradle"
        /
        "wrapper"
    )

    wrapper.mkdir(
        parents=True
    )

    (
        wrapper
        /
        "gradle-wrapper.properties"
    ).write_text(
        "distributionUrl="
        +
        wrapper_url
        +
        "\n"
    )

    (
        root
        /
        "build.gradle"
    ).write_text(
        "buildscript {\n"
        "  dependencies {\n"
        "    classpath "
        "\"com.android.tools.build:gradle:"
        +
        agp
        +
        "\"\n"
        "  }\n"
        "}\n"
    )

    return root


def test_localhost_wrapper_repair():

    with TemporaryDirectory() as tmp:

        root = project(
            tmp,
            "http\\://localhost:8000/"
            "gradle-8.2-all.zip",
            "8.2.0",
        )

        result = (
            GradleCompatibility()
            .repair(
                root
            )
        )

        assert result[
            "changed"
        ]

        assert (
            result[
                "after"
            ][
                "gradle_version"
            ]
            ==
            "8.2"
        )

        assert not (
            result[
                "after"
            ][
                "local_distribution_url"
            ]
        )

        assert (
            "services.gradle.org"
            in
            result[
                "after"
            ][
                "distribution_url"
            ]
        )


def test_agp8_gradle7_upgrade():

    with TemporaryDirectory() as tmp:

        root = project(
            tmp,
            "https\\://services.gradle.org/"
            "distributions/"
            "gradle-7.3.2-all.zip",
            "8.0.2",
        )

        result = (
            GradleCompatibility()
            .repair(
                root
            )
        )

        assert result[
            "changed"
        ]

        assert (
            result[
                "before"
            ][
                "gradle_too_old"
            ]
            is True
        )

        assert (
            result[
                "after"
            ][
                "gradle_version"
            ]
            ==
            "8.0"
        )

        assert (
            result[
                "after"
            ][
                "gradle_too_old"
            ]
            is False
        )


def test_compatible_wrapper_unchanged():

    with TemporaryDirectory() as tmp:

        root = project(
            tmp,
            "https\\://services.gradle.org/"
            "distributions/"
            "gradle-8.2-all.zip",
            "8.0.2",
        )

        result = (
            GradleCompatibility()
            .repair(
                root
            )
        )

        assert (
            result[
                "changed"
            ]
            is False
        )

        assert not result[
            "actions"
        ]


def test_version_tuple_not_float():

    compat = (
        GradleCompatibility()
    )

    assert (
        compat.version_tuple(
            "8.10.2"
        )
        >
        compat.version_tuple(
            "8.9"
        )
    )
