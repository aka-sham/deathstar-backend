#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel
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


class Empire(BaseModel):
    """
    Empire base model.
    """

    # Number of days before the Death Star annihilates Endor.
    countdown: int
    # List of all locations where Bounty Hunter are scheduled to be present.
    bounty_hunters: list[BountyHunter]
