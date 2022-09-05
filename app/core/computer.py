#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx

from app.models import UniverseRoute
from app.settings import MILLENIUM_FALCON_SETTINGS


async def generate_graph_from_routes() -> nx.Graph:
    graph = nx.Graph()
    routes: list[UniverseRoute] = await UniverseRoute.objects()

    for route in routes:
        if MILLENIUM_FALCON_SETTINGS.autonomy >= route.travel_time:
            graph.add_weighted_edges_from(
                [(route.origin, route.destination, route.travel_time)]
            )

    return graph


async def print_shortest_path():
    universe_graph = await generate_graph_from_routes()
    for short_path in nx.shortest_simple_paths(
        universe_graph,
        source=MILLENIUM_FALCON_SETTINGS.departure,
        target=MILLENIUM_FALCON_SETTINGS.arrival,
        weight="weight",
    ):
        print(short_path)
        print(nx.path_weight(universe_graph, short_path, weight="weight"))

        weights = nx.get_edge_attributes(universe_graph, "weight")
        print(weights[tuple(short_path[0:2])])

        print(nx.path_weight(universe_graph, short_path[0:3], weight="weight"))
