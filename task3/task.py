import json
import numpy as np

def main(ranking1_json, ranking2_json):
    data_a = json.loads(ranking1_json)
    data_b = json.loads(ranking2_json)
    
    def get_all_elements(ranking):
        elements = []
        for item in ranking:
            if isinstance(item, list):
                elements.extend(item)
            else:
                elements.append(item)
        return elements

    objects_list = sorted(list(set(get_all_elements(data_a) + get_all_elements(data_b))))
    n = len(objects_list)
    idx_map = {obj: i for i, obj in enumerate(objects_list)}
    
    def get_relation_matrix(ranking):
        matrix = np.zeros((n, n), dtype=int)
        clusters = [c if isinstance(c, list) else [c] for c in ranking]
        
        for i, current_cluster in enumerate(clusters):
            for item_i in current_cluster:
                idx_i = idx_map[item_i]
                for item_j in current_cluster:
                    matrix[idx_i][idx_map[item_j]] = 1
                
                for j in range(i + 1, len(clusters)):
                    for item_j in clusters[j]:
                        matrix[idx_i][idx_map[item_j]] = 1
        return matrix

    y_a = get_relation_matrix(data_a)
    y_b = get_relation_matrix(data_b)
    
    conflicts = np.logical_or(
        np.logical_and(y_a, y_b.T),
        np.logical_and(y_a.T, y_b)
    ).astype(int)
    
    c_matrix = np.logical_and(y_a, y_b).astype(int)
    for i in range(n):
        for j in range(i + 1, n):
            if conflicts[i][j] == 0:
                c_matrix[i][j] = 1
                c_matrix[j][i] = 1

    e_matrix = np.logical_and(c_matrix, c_matrix.T).astype(int)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                e_matrix[i][j] = e_matrix[i][j] or (e_matrix[i][k] and e_matrix[k][j])
    
    visited = [False] * n
    final_clusters = []
    for i in range(n):
        if not visited[i]:
            group = []
            for j in range(n):
                if e_matrix[i][j] == 1:
                    group.append(objects_list[j])
                    visited[j] = True
            final_clusters.append(sorted(group))

    m = len(final_clusters)
    order_matrix = np.zeros((m, m), dtype=int)
    for i in range(m):
        for j in range(m):
            if i != j:
                if c_matrix[idx_map[final_clusters[i][0]]][idx_map[final_clusters[j][0]]] == 1:
                    order_matrix[i][j] = 1

    in_degree = [0] * m
    for i in range(m):
        for j in range(m):
            if i != j and order_matrix[j][i] == 1:
                in_degree[i] += 1
    
    queue = [i for i in range(m) if in_degree[i] == 0]
    sorted_indices = []
    while queue:
        curr = queue.pop(0)
        sorted_indices.append(curr)
        for neighbor in range(m):
            if order_matrix[curr][neighbor] == 1 and curr != neighbor:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    output = []
    for idx in sorted_indices:
        target = final_clusters[idx]
        output.append(target if len(target) > 1 else target[0])
    
    return json.dumps(output, ensure_ascii=False)
