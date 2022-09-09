#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
# Project          : deathstar-backend
# FileName         : compute.py
# -----------------------------------------------------------------------------
# Author           : Sébastien Metzger
# E-Mail           : sebastien.metzger@nomogi.org
##

import logging
import networkx as nx

from app.settings import MilleniumFalconSettings
from app.settings import MILLENIUM_FALCON_SETTINGS
from app.core.models import UniverseRoute
from app.core.models import EmpireSettings
from app.core.models import MilleniumFalconState

# Logger
LOG = logging.getLogger("falcon.core")


async def generate_graph_from_routes(
    millenium_falcon_settings: MilleniumFalconSettings = MILLENIUM_FALCON_SETTINGS,
) -> nx.Graph:
    """
    Generates a weighted undirected graph where each node is a planet and each edge -with weight- represents the distance between 2 planets.


    Args:
        millenium_falcon_settings (MilleniumFalconSettings, optional): Millenium Falcon settings to determine which routes can be kept. Defaults to MILLENIUM_FALCON_SETTINGS.

    Returns:
        nx.Graph: NetworkX Graph which represents all Universe
    """
    LOG.debug("Generates a new graph from routes")
    graph = nx.Graph()
    routes: list[UniverseRoute] = await UniverseRoute.objects()

    for route in routes:
        if millenium_falcon_settings.autonomy >= route.travel_time:
            graph.add_weighted_edges_from(
                [(route.origin, route.destination, route.travel_time)]
            )

    return graph


def bounty_hunter_probability(attempts: int) -> float:
    """
    Generates probability bounty hunters capture the Millenium Falcon
    according to the attempts.

    Args:
        attempts (int): number of attempts to capture the Millenium Falcon.

    Returns:
        float: probability to capture the Millenium Falcon.
    """
    if attempts == 0:
        probability = 0.0
    else:
        probability = 1 / 10

    if attempts > 1:
        for capture_attempt in range(1, attempts):
            probability += (9**capture_attempt) / (10 ** (capture_attempt + 1))

    return probability * 100.0


async def analyse_paths(
    empire_settings: EmpireSettings,
    millenium_falcon_settings: MilleniumFalconSettings = MILLENIUM_FALCON_SETTINGS,
) -> float:
    """
    Analyses all possible paths and return the minimum probability that bounty hunters will capture the Millenium Falcon.

    First all shortest paths ordered by distance are extracted from the Universe graph. Then for each path, a binary tree is created to represents all possible actions according to constraints. Note: a binary tree is enought because there are only 2 actions, Travel and Wait 1 day. Waiting 1 day is similar to Refuel.

    Args:
        empire_settings (EmpireSettings): Empire settings received which described
        the countdown and the future location of bounty hunters.
        millenium_falcon_settings (MilleniumFalconSettings, optional): Millenium Falcon settings to determine which routes can be kept. Defaults to MILLENIUM_FALCON_SETTINGS.

    Returns:
        float: minimum -or worse- probability that bounty hunters will capture the Millenium Falcon.
    """

    # List of bounty hunter probabilities for each shortest path where each possible routes have been treated
    probabilities = [100.0]
    universe_graph = await generate_graph_from_routes(millenium_falcon_settings)
    shortest_paths = nx.shortest_simple_paths(
        universe_graph,
        source=millenium_falcon_settings.departure,
        target=millenium_falcon_settings.arrival,
        weight="weight",
    )

    # Dictionary of distances keyed by edge
    basic_distances = nx.get_edge_attributes(universe_graph, "weight")
    # Extra key to use dictionnary correctly
    extra_distances = {}
    for key, value in basic_distances.items():
        if len(key) == 2:
            extra_distances[(key[1], key[0])] = value
    # Complete dictionnary of distances
    distances = basic_distances | extra_distances

    for shortest_path in shortest_paths:
        # Minimal distance needed to travel from departure to arrival
        # without refueling
        min_distance = nx.path_weight(universe_graph, shortest_path, weight="weight")

        if min_distance <= empire_settings.countdown:
            departure_state = MilleniumFalconState(
                planet=millenium_falcon_settings.departure,
                day=0,
                fuel=millenium_falcon_settings.autonomy,
                capture_attempts=0,
            )
            probabilities.append(
                travel_trought_space(
                    departure_state,
                    shortest_path,
                    distances,
                    empire_settings,
                    millenium_falcon_settings,
                )
            )

    return min(probabilities)


def travel_trought_space(
    state: MilleniumFalconState,
    path: list[str],
    distances: dict,
    empire_settings: EmpireSettings,
    millenium_falcon_settings: MilleniumFalconSettings = MILLENIUM_FALCON_SETTINGS,
) -> float:
    """
    Recursive method to travel through the whole possibilities on a given path.
    It will walkthrough a binary tree generated thanks to 2 possible
    actions, travel or wait. Then when a leaf is reached it will return
    the bounty hunter probability if this leaf is the destination, or 100% chance
    to failed if the leaf represent a planet where countdown is finished.

    Args:
        state (MilleniumFalconState): Millenium Falcon current state.
        path (list[str]): current path on which Millenium Falcon is travelling.
        distances (dict): contains all distances between planets.
        empire_settings (EmpireSettings): Empire settings received which described
        the countdown and the future location of bounty hunters.
        millenium_falcon_settings (MilleniumFalconSettings, optional): Millenium Falcon settings to determine which routes can be kept. Defaults to MILLENIUM_FALCON_SETTINGS.

    Returns:
        float: probability that bounty hunters will capture the Millenium Falcon.
    """
    if state.planet == path[-1]:
        return bounty_hunter_probability(state.capture_attempts)
    elif state.day == empire_settings.countdown:
        return 100.0
    else:
        # Travel
        travel_probability = 100.0
        next_planet = path[path.index(state.planet) + 1]
        distance = distances[(state.planet, next_planet)]

        if distance <= state.fuel and state.day + distance <= empire_settings.countdown:
            travel_state = MilleniumFalconState.copy(state)
            travel_state.planet = next_planet
            travel_state.fuel -= distance
            travel_state.day += distance
            travel_state.capture_attempts = get_capture_attempts(
                travel_state,
                empire_settings,
            )
            travel_probability = travel_trought_space(
                travel_state,
                path,
                distances,
                empire_settings,
                millenium_falcon_settings,
            )

        # Wait
        wait_state = MilleniumFalconState.copy(state)
        wait_state.planet = state.planet
        wait_state.fuel = millenium_falcon_settings.autonomy
        wait_state.day += 1
        wait_state.capture_attempts = get_capture_attempts(
            wait_state,
            empire_settings,
        )
        wait_probability = travel_trought_space(
            wait_state,
            path,
            distances,
            empire_settings,
            millenium_falcon_settings,
        )

        return min([travel_probability, wait_probability])


def get_capture_attempts(
    state: MilleniumFalconState, empire_settings: EmpireSettings
) -> int:
    """
    Determines depending on the Millenium Falcon state
    and bounty hunters planning if they will try to capture the Millenium Falcon.

    Args:
        state (MilleniumFalconState): Millenium Falcon current state.
        empire_settings (EmpireSettings): Empire settings which contains the countdown and bounty hunters positions.

    Returns:
        int: update capture attempts number.
    """
    nb_attempts = state.capture_attempts
    for bounty_hunter in empire_settings.bounty_hunters:
        if bounty_hunter.planet == state.planet and bounty_hunter.day == state.day:
            nb_attempts += 1

    return nb_attempts
