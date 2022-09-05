#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Any

from pydantic import BaseSettings
from pydantic import BaseModel


def millenium_falcon_json_settings(settings: BaseSettings) -> dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.
    """
    encoding = settings.__config__.env_file_encoding
    return json.loads(Path("millennium-falcon.json").read_text(encoding))


def empire_json_settings(settings: BaseSettings) -> dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.
    """
    encoding = settings.__config__.env_file_encoding
    return json.loads(Path("empire.json").read_text(encoding))


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


class BountyHunter(BaseModel):
    # Name of the planet.
    planet: str
    # Day the bounty hunters are on the planet.
    day: int


class EmpireSettings(BaseSettings):
    """
    Empire Settings derived from pydantic settings management class.
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
                empire_json_settings,
                init_settings,
                env_settings,
                file_secret_settings,
            )

    # Number of days before the Death Star annihilates Endor.
    countdown: int
    # List of all locations where Bounty Hunter are scheduled to be present.
    bounty_hunters: list[BountyHunter]


# Default app settings
MILLENIUM_FALCON_SETTINGS = MilleniumFalconSettings(
    autonomy=6, departure="Tatooine", arrival="Endor", routes_db="universe.db"
)

EMPIRE_SETTINGS = EmpireSettings(
    countdown=6,
    bounty_hunters=[
        BountyHunter(planet="Tatooine", day=4),
        BountyHunter(planet="Dagobah", day=5),
    ],
)
