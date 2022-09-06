#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from starlite import Starlite
from starlite import get
from starlite import post
from starlite import Body
from starlite import UploadFile
from starlite import RequestEncodingType
from starlite.plugins.piccolo_orm import PiccoloORMPlugin

from app.models import UniverseRoute
from app.core.models import EmpireSettings
from app.core.compute import analyse_paths


@get("/")
async def health_check() -> str:
    await print_shortest_path()
    return "healthy"


@get("/routes")
async def retrieve_routes() -> list[UniverseRoute]:
    return await UniverseRoute.select()


@post("/file-upload")
async def handle_file_upload(
    data: UploadFile = Body(media_type=RequestEncodingType.MULTI_PART),
) -> None:
    contents = await data.read()
    empire_settings = EmpireSettings.parse_raw(
        contents, content_type="application/json"
    )
    proba = await analyse_paths(empire_settings)


app = Starlite(
    route_handlers=[health_check, retrieve_routes, handle_file_upload],
    plugins=[PiccoloORMPlugin()],
)
