import heapq
import os
import pickle
from collections import defaultdict
from typing import List

import networkx


def chinese_postman(G_directed: networkx.MultiDiGraph, start_node):
    G = G_directed.to_undirected()

    print("Step 1")
    # Identifier les sommets de degré impair
    odd_nodes = [node for node, degree in G.degree() if degree % 2 != 0]

    print("Step 2")
    # Calculer les distances minimales entre paires de sommets impairs
    shortest_paths_file = "../shortest_paths.pkl"

    if not os.path.exists(shortest_paths_file):
        print("Calcul des plus courts chemins entre sommets impairs...")
        all_lengths = dict(networkx.all_pairs_dijkstra_path_length(G, weight="length"))
        shortest_paths = {}
        for u in odd_nodes:
            for v in odd_nodes:
                if u != v and v in all_lengths[u]:
                    if u not in shortest_paths:
                        shortest_paths[u] = {}
                    shortest_paths[u][v] = all_lengths[u][v]
        with open(shortest_paths_file, "wb") as f:
            pickle.dump(shortest_paths, f)
    else:
        print("Chargement des distances depuis cache...")
        with open(shortest_paths_file, "rb") as f:
            shortest_paths = pickle.load(f)

    print("Step 3")
    # Construire le graphe complet pondéré entre les sommets impairs
    odd_G = networkx.Graph()
    for u in shortest_paths:
        for v in shortest_paths[u]:
            odd_G.add_edge(u, v, weight=shortest_paths[u][v])

    print("Step 4")
    # Calculer le matching parfait de poids minimal
    matching = networkx.algorithms.matching.min_weight_matching(odd_G, weight="weight")

    print("Step 5")
    # Ajouter les chemins du matching dans le graphe original
    for u, v in matching:
        path = networkx.shortest_path(G, source=u, target=v, weight="length")
        for i in range(len(path) - 1):
            u1, v1 = path[i], path[i + 1]
            edge_data = list(G[u1][v1].values())[0]
            G.add_edge(u1, v1, **edge_data)

    print("Step 6")
    # 8. Générer le circuit eulérien depuis la mairie
    if networkx.is_eulerian(G):
        euler_circuit = list(networkx.eulerian_circuit(G, source=start_node))
        euler_path = [u for u, v in euler_circuit] + [euler_circuit[-1][1]]
    else:
        print("Le graphe n'est pas eulérien.")
        euler_path = None

    return euler_path


def dijkstra(times: List[List[int]], n: int, k: int) -> int:
    h = []
    dists = [float("+inf")] * n
    dists[k - 1] = 0

    edges = defaultdict(list)

    for i in range(len(times)):
        ui, vi, ti = times[i]
        edges[ui].append((vi, ti))

    heapq.heappush(h, (0, k))

    while h:
        dist, node = heapq.heappop(h)
        for vi, ti in edges[node]:
            d = dist + ti
            if d < dists[vi - 1]:
                dists[vi - 1] = d
                heapq.heappush(h, (dists[vi - 1], vi))

    if any(d == float("inf") for d in dists):
        return -1
    return max(dists)
