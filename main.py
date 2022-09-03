#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from starlite import Starlite, get


@get(path="/")
async def health_check() -> str:
    return "healthy"


app = Starlite(route_handlers=[health_check])
