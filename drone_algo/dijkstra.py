import heapq
from typing import List
from collections import defaultdict


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
