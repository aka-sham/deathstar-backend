#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import BaseModel


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
