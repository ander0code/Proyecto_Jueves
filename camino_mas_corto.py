import networkx as nx

def calcular_camino_mas_corto(graph, nodo_inicio, nodo_fin):
    """
    Calcula el camino más corto en un grafo utilizando el algoritmo de Dijkstra.

    Args:
    - graph: Grafo en el que se calculará el camino.
    - nodo_inicio: Nodo de inicio.
    - nodo_fin: Nodo de destino.

    Returns:
    - shortest_path: Lista de nodos que representan el camino más corto.
    """
    try:
        shortest_path = nx.dijkstra_path(graph, nodo_inicio, nodo_fin, weight='weight')
        return shortest_path
    except nx.NetworkXNoPath:
        print(f"No hay camino entre {nodo_inicio} y {nodo_fin}")
        return None