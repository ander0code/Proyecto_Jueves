import networkx as nx

def calcular_camino_mas_corto(graph, nodo_inicio, nodo_fin):

    try:
        shortest_path = nx.dijkstra_path(graph, nodo_inicio, nodo_fin, weight='weight')
        return shortest_path
    except nx.NetworkXNoPath:
        print(f"No hay camino entre {nodo_inicio} y {nodo_fin}")
        return None