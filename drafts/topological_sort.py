from functools import reduce


def recursive_dfs(graph, start, path=None):
    '''recursive depth first search from start'''
    if path is None:
        path = []
    path = path + [start]
    for node in graph[start]:
        if not node in path:
            path = recursive_dfs(graph, node, path)
    return path


def iterative_dfs(graph, start, path=None):
    '''iterative depth first search from start'''
    if path is None:
        path = []
    q = [start]
    while q:
        v = q.pop(0)
        if v not in path:
            path = path + [v]
            q = graph[v] + q
    return path


def iterative_bfs(graph, start, path=None):
    '''iterative breadth first search from start'''
    if path is None:
        path = []
    q = [start]
    while q:
        v = q.pop(0)
        if not v in path:
            path = path + [v]
            q = q + graph[v]
    return path


def iterative_topological_sort(graph, start):
    seen = set()
    stack = []  # path variable is gone, stack and order are new
    order = []  # order will be in reverse order at first
    q = [start]
    while q:
        v = q.pop()
        if v not in seen:
            seen.add(v)  # no need to append to path any more
            q.extend(graph[v])

            while stack and v not in graph[stack[-1]]:  # new stuff here!
                order.append(stack.pop())
            stack.append(v)

    return stack + order[::-1]  # new return value!


def recursive_topological_sort(graph, node):
    result = []
    seen = set()

    def recursive_helper(node):
        for neighbor in graph[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                recursive_helper(neighbor)
        result.insert(0, node)  # this line replaces the result.append line

    recursive_helper(node)
    return result


# '''
#    +---- A
#    |   /   \
#    |  B--D--C
#    |   \ | /
#    +---- E
# '''

# graph = {
#     'A': ['B', 'C'],
#     'B': ['D', 'E'],
#     'C': ['D', 'E'],
#     'D': ['E'],
#     'E': ['A']
# }

graph = {
    "A": ["D"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": []
}

print('recursive dfs ', recursive_dfs(graph, 'B'))
print('iterative dfs ', iterative_dfs(graph, 'B'))
print('iterative bfs ', iterative_bfs(graph, 'B'))
print('topological sort ', iterative_topological_sort(graph, 'B'))
print('recursive sort ', recursive_topological_sort(graph, 'B'))

# graph = {
#     "A": ["D"],
#     "B": ["A", "D"],
#     "C": ["A", "D"],
#     "D": []
# }


graph = {
    "A": set(["D"]),
    "B": set(["A", "D"]),
    "C": set(["A", "D"]),
    "D": set([])
}

def toposort2(data):
    for k, v in data.items():
        # v.discard(k)  # Ignore self dependencies
        if k in v:
            v.remove(k)  # Ignore self dependencies
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    data.update({item: set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield ' '.join(sorted(ordered))
        data = {item: (dep - ordered) for item, dep in data.items()
                if item not in ordered}
    assert not data, "A cyclic dependency exists amongst %r" % data


from graphlib import TopologicalSorter

print('\n'.join(toposort2(graph)))
print(tuple(TopologicalSorter(graph).static_order()))
