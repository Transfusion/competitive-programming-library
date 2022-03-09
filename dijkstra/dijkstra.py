from collections import defaultdict
import heapq, math
from typing import Dict, Tuple, TypeVar

T = TypeVar("T")


def dijkstra(graph: Dict[T, Tuple[T, float]], start: T):
    """https://judge.yosupo.jp/submission/81491"""
    pq = [[0, start]]
    visited = set()
    dists = defaultdict(lambda: math.inf)
    dists[start] = 0
    parent = {}

    while pq:
        shortest_dist, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        for v, w in graph[node]:
            if dists[node] + w < dists[v]:
                dists[v] = dists[node] + w
                parent[v] = node
                heapq.heappush(pq, [dists[v], v])

    obj = lambda: None
    obj.dists = dists
    obj.parent = parent
    return obj
