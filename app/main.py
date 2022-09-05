#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
from starlite import Starlite, get
from starlite.plugins.piccolo_orm import PiccoloORMPlugin

from app.models import UniverseRoute
from app.core.computer import print_shortest_path


@get(path="/")
async def health_check() -> str:
    await print_shortest_path()
    return "healthy"


@get("/routes")
async def retrieve_routes() -> list[UniverseRoute]:
    return await UniverseRoute.select()


app = Starlite(
    route_handlers=[health_check, retrieve_routes], plugins=[PiccoloORMPlugin()]
)
