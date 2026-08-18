#!/usr/bin/env python3

import os
from pathlib import Path


class ReleaseSigning:

    ENV = {
        "keystore":
        "ANBE_KEYSTORE",

        "store_password":
        "ANBE_KEYSTORE_PASSWORD",

        "key_alias":
        "ANBE_KEY_ALIAS",

        "key_password":
        "ANBE_KEY_PASSWORD",
    }


    GRADLE_ENV = {
        "keystore":
        "ORG_GRADLE_PROJECT_ANBE_RELEASE_STORE_FILE",

        "store_password":
        "ORG_GRADLE_PROJECT_ANBE_RELEASE_STORE_PASSWORD",

        "key_alias":
        "ORG_GRADLE_PROJECT_ANBE_RELEASE_KEY_ALIAS",

        "key_password":
        "ORG_GRADLE_PROJECT_ANBE_RELEASE_KEY_PASSWORD",
    }


    def read(self):

        return {
            name:
            os.environ.get(
                env_name
            )

            for name, env_name
            in self.ENV.items()
        }


    def configured(self):

        return (
            self.validate()
            .get(
                "configured"
            )
            is True
        )


    def validate(self):

        data = self.read()

        missing = [
            env_name

            for name, env_name
            in self.ENV.items()

            if not data.get(
                name
            )
        ]

        if missing:

            return {
                "configured":
                False,

                "missing":
                missing,
            }

        keystore = (
            Path(
                data[
                    "keystore"
                ]
            )
            .expanduser()
        )

        if not keystore.exists():

            return {
                "configured":
                False,

                "missing":
                [],

                "error":
                "Keystore not found: "
                +
                str(
                    keystore
                ),
            }

        return {
            "configured":
            True,

            "keystore":
            str(
                keystore.resolve()
            ),

            "key_alias":
            data[
                "key_alias"
            ],
        }


    def gradle_environment(self):

        data = self.read()

        status = self.validate()

        if not status.get(
            "configured"
        ):

            return {}

        keystore = (
            Path(
                data[
                    "keystore"
                ]
            )
            .expanduser()
            .resolve()
        )

        values = {
            "keystore":
            str(
                keystore
            ),

            "store_password":
            data[
                "store_password"
            ],

            "key_alias":
            data[
                "key_alias"
            ],

            "key_password":
            data[
                "key_password"
            ],
        }

        return {
            self.GRADLE_ENV[
                name
            ]:
            value

            for name, value
            in values.items()
        }
