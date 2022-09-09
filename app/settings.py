#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
# Project          : deathstar-backend
# FileName         : settings.py
# -----------------------------------------------------------------------------
# Author           : Sébastien Metzger
# E-Mail           : sebastien.metzger@nomogi.org
##

import json
from pathlib import Path
from typing import Any

from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


def millenium_falcon_json_settings(settings: BaseSettings) -> dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.
    """
    encoding = settings.__config__.env_file_encoding
    return json.loads(Path("millennium-falcon.json").read_text(encoding))


class MilleniumFalconSettings(BaseSettings):
    """
    Millenium Falcon Settings derived from pydantic settings management class.
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
                millenium_falcon_json_settings,
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


class AppSettings(BaseSettings):
    """Settings class to setup application."""

    app_host: str
    app_port: int
    app_reload: bool
    cors_allow_origins: str

    class Config:
        """Overrides Config class to read .env file correctly."""

        env_file = ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings


# Default Millenium Falcon settings
MILLENIUM_FALCON_SETTINGS = MilleniumFalconSettings(
    autonomy=6, departure="Tatooine", arrival="Endor", routes_db="universe.db"
)

# Default Millenium Falcon settings
APP_SETTINGS = AppSettings(
    app_host="127.0.0.1", app_port=8000, app_reload=False, cors_allow_origins="*"
)

# EOF
