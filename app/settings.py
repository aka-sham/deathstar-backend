#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Any

from pydantic import BaseSettings


def json_config_settings_source(settings: BaseSettings) -> dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `millennium-falcon.json`
    """
    encoding = settings.__config__.env_file_encoding
    return json.loads(Path("millennium-falcon.json").read_text(encoding))


class AppSettings(BaseSettings):
    """
    Application Settings derived from pydantic settings management class.
    """

    class Config:
        env_file_encoding = "utf-8"
        case_sensitive = True

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                json_config_settings_source,
                init_settings,
                env_settings,
                file_secret_settings,
            )

    # Autonomy of the Millennium Falcon in days.
    autonomy: int
    # Planet where the Millennium Falcon is on day 0.
    departure: str
    # Planet where the Millennium Falcon must be at or before countdown.
    arrival: str
    # Path toward a SQLite database file containing the routes.
    routes_db: str


# Default app settings
app_settings = AppSettings(
    autonomy=6, departure="Tatooine", arrival="Endor", routes_db="universe.db"
)
