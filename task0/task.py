from typing import List, Set, Dict

def main(s: str) -> List[List[bool]]:
    
    edges = []
    nodes = set()
    
    
    for line in s.strip().split("\n"):
        if not line:
            continue
        u, v = line.strip().split(",")
        edges.append((u, v))
        nodes.update([u, v])

    
    nodes_list = sorted(list(nodes))
    node_to_idx: Dict[str, int] = {node: idx for idx, node in enumerate(nodes_list)}
    n = len(nodes_list)

    
    adjacency_matrix = [[False] * n for _ in range(n)]
    for u, v in edges:
        i, j = node_to_idx[u], node_to_idx[v]
        adjacency_matrix[i][j] = True

    return adjacency_matrix


with open("task2.csv", "r", encoding="utf-8") as f:
        csv_data = f.read()
        
result_matrix = main(csv_data)


for row in result_matrix:
    print([int(x) for x in row])


