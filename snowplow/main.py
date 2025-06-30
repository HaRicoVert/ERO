#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox

from common.utils import SNOWPLOW_TYPE_2, SNOWPLOW_TYPE_1, colors, split_graph
from drone.main import graph
from drone.utils import calcul_cout
from snowplow.utils import solve_single_ultra_fast


def assign_sectors(n_vehicles, n_sectors=5):
    assignments = [[] for _ in range(n_vehicles)]
    for i in range(n_sectors):
        assignments[i % n_vehicles].append(i)
    return assignments


def run_strategy(vehicles, start_node, sector_graphs):
    results = {}
    assignments = assign_sectors(len(vehicles), len(sector_graphs))

    fig, ax = plt.subplots(figsize=(15, 15))
    ox.plot_graph(
        nx.compose_all(sector_graphs),
        ax=ax,
        node_size=0,
        edge_color="#dddddd",
        edge_linewidth=0.8,
        show=False,
        close=False,
    )

    for i, vehicle in enumerate(vehicles):
        total_distance = 0
        total_time = 0
        assigned_edges = []
        color = colors[i % len(colors)](0.8)

        for sector_idx in assignments[i]:
            g = sector_graphs[sector_idx]
            result = solve_single_ultra_fast(g, list(g.edges(keys=True)), vehicle)

            if start_node in g.nodes:
                sector_start = start_node
            else:
                sector_start = list(g.nodes)[0]

            x1, y1 = g.nodes[sector_start]["x"], g.nodes[sector_start]["y"]
            x2, y2 = (
                g.nodes[result["start_node"]]["x"],
                g.nodes[result["start_node"]]["y"],
            )
            return_dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            return_time = (return_dist / 1000) / vehicle.average_speed

            total_distance += result["distance"] + (2 * return_dist / 1000)
            total_time += result["temps_utilise"] + (2 * return_time)
            assigned_edges.extend(result["aretes_assignees"])

            for u, v, k in result["aretes_assignees"]:
                if g.has_edge(u, v, k):
                    xs = [g.nodes[u]["x"], g.nodes[v]["x"]]
                    ys = [g.nodes[u]["y"], g.nodes[v]["y"]]
                    ax.plot(xs, ys, color=color, linewidth=2.5)

        results[f"vehicle{i + 1}"] = {
            "distance": total_distance,
            "time": total_time,
        }

    plt.show()
    return results


from itertools import product


def main():
    vehicle_types = [SNOWPLOW_TYPE_1, SNOWPLOW_TYPE_2]

    sector_graphs = split_graph(graph)
    start_node = next(iter(graph.nodes()))

    print("=== RÉSULTATS POUR TOUTES LES COMBINAISONS DE VÉHICULES ===\n")

    for nb_vehicles in range(1, 5):
        print(f"--- {nb_vehicles} véhicule(s) ---")

        for combo in product(vehicle_types, repeat=nb_vehicles):
            vehicles = list(combo)

            results = run_strategy(
                vehicles[: len(sector_graphs)], start_node, sector_graphs
            )

            combo_str = ", ".join(
                [f"Type{1 if v == SNOWPLOW_TYPE_1 else 2}" for v in vehicles]
            )
            print(f"\nCombinaison: [{combo_str}]")

            cout_total_global = 0
            distance_totale = 0
            temps_list = []

            for i in range(len(vehicles)):
                r = results.get(f"vehicle{i + 1}", {})
                distance = r.get("distance", 0)
                temps = r.get("time", 0)
                cout_total = calcul_cout(vehicles[i], distance)[1]
                cout_total_global += cout_total
                distance_totale += distance
                temps_list.append(temps)

                print(
                    f"  Véhicule {i + 1}: {distance:.1f} km, {temps:.1f} h, Coût: {cout_total:.2f} €"
                )

            temps_max = max(temps_list) if temps_list else 0
            print(
                f"  TOTAL: {distance_totale:.1f} km, Temps max: {temps_max:.1f} h, Coût total: {cout_total_global:.2f} €"
            )

        print()


if __name__ == "__main__":
    main()
