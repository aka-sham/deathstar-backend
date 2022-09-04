#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from starlite import Starlite, get
from starlite.plugins.piccolo_orm import PiccoloORMPlugin

from app.models import UniverseRoute
from app.settings import app_settings


@get(path="/")
async def health_check() -> str:
    return "healthy"


@get("/routes")
async def retrieve_routes() -> list[UniverseRoute]:
    return await UniverseRoute.select()


print(app_settings)
app = Starlite(
    route_handlers=[health_check, retrieve_routes], plugins=[PiccoloORMPlugin()]
)
