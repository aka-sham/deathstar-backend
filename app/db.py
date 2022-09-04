#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from piccolo.engine.sqlite import SQLiteEngine
from app.settings import app_settings

DB = SQLiteEngine(path=app_settings.routes_db)
