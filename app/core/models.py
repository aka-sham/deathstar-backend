#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
# Project          : deathstar-backend
# FileName         : models.py
# -----------------------------------------------------------------------------
# Author           : Sébastien Metzger
# E-Mail           : sebastien.metzger@nomogi.org
##

from pydantic import BaseModel
from pydantic import BaseConfig

from starlite import UploadFile

from piccolo.columns.column_types import (
    Integer,
    Varchar,
)
from piccolo.table import Table

from app.db import DB


class UniverseRoute(Table, tablename="routes", db=DB):
    origin = Varchar(primary_key=True)
    destination = Varchar(primary_key=True)
    travel_time = Integer()


class BountyHunter(BaseModel):
    # Name of the planet.
    planet: str
    # Day the bounty hunters are on the planet.
    day: int


class EmpireSettings(BaseModel):
    """
    Empire base model.
    """

    # Number of days before the Death Star annihilates Endor.
    countdown: int
    # List of all locations where Bounty Hunter are scheduled to be present.
    bounty_hunters: list[BountyHunter]


class MilleniumFalconState(BaseModel):
    planet: str
    day: int
    fuel: int
    capture_attempts: int


class C3PORequest(BaseModel):
    empire: UploadFile

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class R2D2Request(BaseModel):
    millenium_falcon: UploadFile
    empire: UploadFile

    class Config(BaseConfig):
        arbitrary_types_allowed = True


class Mission(BaseModel):
    probability: float
