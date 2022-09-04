#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from starlite import Starlite, get
from app.settings import app_settings


@get(path="/")
async def health_check() -> str:
    return "healthy"


print(app_settings)
app = Starlite(route_handlers=[health_check])
