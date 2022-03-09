#ifndef __STD_VECTOR__
#define __STD_VECTOR__
#include <vector>
#endif

#ifndef __STD_QUEUE__
#define __STD_QUEUE__
#include <queue>
#endif

#ifndef __STD_SET__
#define __STD_SET__
#include <set>
#endif

#ifndef __STD_TUPLE__
#define __STD_TUPLE__
#include <tuple>
#endif

#ifndef __STD_UNORDERED_MAP__
#define __STD_UNORDERED_MAP__
#include <unordered_map>
#endif

template <typename T, typename V>
struct dijkstra_return
{
    std::unordered_map<T, V> dists;
    std::unordered_map<T, T> parent;
};

// https://judge.yosupo.jp/submission/81531
// V should be a numeric type like int, float, or double
template <typename T, typename V>
dijkstra_return<T, V> dijkstra(std::unordered_map<T, std::vector<std::pair<T, V>>> graph, T start)
{
    std::priority_queue<std::pair<V, T>, std::vector<std::pair<V, T>>, std::greater<std::pair<V, T>>> pq;

    pq.push(std::make_pair(0, start));

    std::unordered_map<T, V> dists;
    std::unordered_map<T, T> parent;
    std::set<T> visited;

    while (!pq.empty())
    {
        std::pair<V, T> item = pq.top();
        pq.pop();
        V shortest_dist = item.first;
        T node = item.second;

        if (visited.count(node) > 0)
        {
            continue;
        }
        visited.insert(node);

        for (std::pair<T, V> child : graph[node])
        {
            T vertex = child.first;
            V weight = child.second;
            V shortest_path_to_v;
            // check if exists, assign infinity if does
            if (dists.find(vertex) == dists.end())
            {
                dists[vertex] = std::numeric_limits<V>::max();
            }
            if (dists[node] + weight < dists[vertex])
            {
                dists[vertex] = dists[node] + weight;
                parent[vertex] = node;
                pq.push(std::make_pair(dists[vertex], vertex));
            }
        }
    }
    dijkstra_return<T, V> res;
    res.dists = dists;
    res.parent = parent;

    return res;
}