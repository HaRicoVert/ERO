def solve_single_ultra_fast(graph, edges, vehicle):
    if not edges:
        return {
            "distance": 0,
            "temps_utilise": 0,
            "cout_total": vehicle.cost_per_day,
            "aretes_assignees": [],
            "start_node": None,
            "status": "Optimal",
        }

    # Algorithme glouton : sélectionner les arêtes par rapport qualité/prix
    valid_edges_data = []

    for edge in edges:
        u, v = edge[0], edge[1]
        key = edge[2] if len(edge) > 2 else 0

        if not graph.has_edge(u, v, key):
            continue

        edge_data = graph[u][v][key]
        length = edge_data.get("length", 1000)
        priority = edge_data.get("priority", 1)  # Priorité de l'arête

        # Score : priorité / longueur (plus court et prioritaire = mieux)
        score = priority / (length / 1000) if length > 0 else 0

        valid_edges_data.append(
            {
                "edge": (u, v, key),
                "length": length,
                "priority": priority,
                "score": score,
            }
        )

    # Trier par score décroissant (glouton)
    valid_edges_data.sort(key=lambda x: x["score"], reverse=True)

    # Sélectionner les arêtes selon contraintes du véhicule
    selected_edges = []
    total_distance = 0
    max_distance_km = (
        vehicle.max_distance_per_day * 1000
        if hasattr(vehicle, "max_distance_per_day")
        else float("inf")
    )

    for edge_data in valid_edges_data:
        if total_distance + edge_data["length"] <= max_distance_km:
            selected_edges.append(edge_data["edge"])
            total_distance += edge_data["length"]
        else:
            break

    # Calculs finaux
    distance_km = total_distance / 1000
    time = distance_km / vehicle.average_speed
    cost = vehicle.cost_per_day + (distance_km * vehicle.cost_per_km)
    start_node = selected_edges[0][0] if selected_edges else None

    return {
        "distance": distance_km,
        "temps_utilise": time,
        "cout_total": cost,
        "aretes_assignees": selected_edges,
        "start_node": start_node,
        "status": "Optimal" if selected_edges else "Erreur",
    }
