from typing import Tuple
import math

def main(s: str, e: str) -> Tuple[float, float]:
    lines = s.strip().split('\n')
    edges = []
    for line in lines:
        a, b = line.split(',')
        edges.append((a.strip(), b.strip()))
    
    root = e.strip()
    
    nodes = set()
    for a, b in edges:
        nodes.add(a)
        nodes.add(b)
    
    graph = {node: [] for node in nodes}
    for a, b in edges:
        graph[a].append(b)
    
    r1 = edges
    
    r2 = [(b, a) for a, b in edges]
    
    r3 = []
    for node in nodes:
        visited = set()
        queue = graph[node][:]
        while queue:
            child = queue.pop(0)
            if child in visited:
                continue
            visited.add(child)
            if child in graph and graph[child]:
                for grandchild in graph[child]:
                    r3.append((node, grandchild))
                    queue.append(grandchild)
    
    r4 = [(b, a) for a, b in r3]
    
    r5 = []
    parent = {}
    for a, b in edges:
        parent[b] = a
    
    for node in nodes:
        if node in parent:
            p = parent[node]
            for sibling in graph.get(p, []):
                if sibling != node:
                    r5.append((node, sibling))
                    r5.append((sibling, node))
    
    n = len(nodes)
    max_links = n - 1
    
    relations = [r1, r2, r3, r4, r5]
    k = len(relations)
    
    H_total = 0.0
    
    for node in nodes:
        for ri in relations:
            lij = sum(1 for a, b in ri if a == node)
            if lij > 0:
                P = lij / max_links
                H_partial = -P * math.log2(P)
                H_total += H_partial
    
    c = 1 / (math.e * math.log(2))
    H_ref = c * n * k
    
    h_norm = H_total / H_ref
    
    return (round(H_total, 1), round(h_norm, 1))
