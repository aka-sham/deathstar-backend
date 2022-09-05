#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from piccolo.engine.sqlite import SQLiteEngine
from app.settings import MILLENIUM_FALCON_SETTINGS

DB = SQLiteEngine(path=MILLENIUM_FALCON_SETTINGS.routes_db)
