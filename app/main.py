#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
# Project          : deathstar-backend
# FileName         : main.py
# -----------------------------------------------------------------------------
# Author           : Sébastien Metzger
# E-Mail           : sebastien.metzger@nomogi.org
##

import logging

from starlite import CORSConfig
from starlite import Starlite
from starlite import post
from starlite import Body
from starlite import RequestEncodingType
from starlite.plugins.piccolo_orm import PiccoloORMPlugin

from app.settings import MilleniumFalconSettings
from app.util import init_logging
from app.core.models import EmpireSettings
from app.core.models import Mission
from app.core.models import C3PORequest
from app.core.models import R2D2Request
from app.core.compute import analyse_paths

# Logger
LOG = logging.getLogger("falcon")

# Allows every origins
CORS_CONFIG = CORSConfig(allow_origins=["*"])


@post("/c3po")
async def handle_c3po_request(
    data: C3PORequest = Body(media_type=RequestEncodingType.MULTI_PART),
) -> Mission:
    """
    Route dedicated to C3PO to return the probability of success to save Endor.

    Args:
        data (C3PORequest, optional): C3PO must upload an empire.json file which contains infos about countdown and bounty hunters locations. Defaults to Body(media_type=RequestEncodingType.MULTI_PART).
    Returns:
        Mission: Mission DTO wich contains the probability of success.
    """
    LOG.info("C3PO asks for an analysis")
    content = await data.empire.read()
    empire_settings = EmpireSettings.parse_raw(content, content_type="application/json")
    probability_to_be_captured = await analyse_paths(empire_settings)
    LOG.info(f"Probability to be captured: {probability_to_be_captured:.2f}%")
    return Mission(probability=100 - probability_to_be_captured)


@post("/r2d2")
async def handle_r2d2_request(
    data: R2D2Request = Body(media_type=RequestEncodingType.MULTI_PART),
) -> Mission:
    """
    Route dedicated to R2D2 to return the probability of success to save Endor.

    Args:
        data (R2D2Request, optional): R2D2 must upload an millenium-falcon.json and an empire.json files. Defaults to Body(media_type=RequestEncodingType.MULTI_PART).

    Returns:
        Mission: Mission DTO wich contains the probability of success.
    """
    LOG.info("R2D2 asks for an analysis")
    millenium_falcon_content = await data.millenium_falcon.read()
    millenium_falcon_settings = MilleniumFalconSettings.parse_raw(
        millenium_falcon_content, content_type="application/json"
    )

    empire_content = await data.empire.read()
    empire_settings = EmpireSettings.parse_raw(
        empire_content, content_type="application/json"
    )

    probability_to_be_captured = await analyse_paths(
        empire_settings, millenium_falcon_settings
    )
    LOG.info(f"Probability to be captured: {probability_to_be_captured:.2f}%")
    return Mission(probability=100 - probability_to_be_captured)


app = Starlite(
    route_handlers=[handle_c3po_request, handle_r2d2_request],
    plugins=[PiccoloORMPlugin()],
    on_startup=[init_logging],
    cors_config=CORS_CONFIG,
)
