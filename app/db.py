#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
# Project          : deathstar-backend
# FileName         : db.py
# -----------------------------------------------------------------------------
# Author           : Sébastien Metzger
# E-Mail           : sebastien.metzger@nomogi.org
##

from piccolo.engine.sqlite import SQLiteEngine
from app.settings import MILLENIUM_FALCON_SETTINGS

# Create DB engine for future connection
DB = SQLiteEngine(path=MILLENIUM_FALCON_SETTINGS.routes_db)

# EOF
