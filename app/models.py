#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
