import networkx as nx
import matplotlib.pyplot as plt
import random
from camino_mas_corto import calcular_camino_mas_corto  # Importar la función para calcular el camino más corto

def crear_grafo_dinamico():
    """
    Crea un grafo dirigido para modelar la dinámica de una partícula.
    
    Returns:
    - G: Grafo con nodos que representan estados de la partícula y aristas con pesos.
    """
    G = nx.DiGraph()  # Usamos un grafo dirigido para simular la trayectoria

    # Estado inicial de la partícula
    posicion_inicial = 0
    velocidad_inicial = 0  # Velocidad inicial en 0
    estado_inicial = (posicion_inicial, velocidad_inicial)
    G.add_node(estado_inicial)

    # Agregar nodos y aristas al grafo
    for paso in range(1, 11):  # Simulación de 10 pasos
        nueva_posicion = paso
        nuevo_estado = (nueva_posicion, velocidad_inicial)
        G.add_node(nuevo_estado)
        G.add_edge(estado_inicial, nuevo_estado, weight=0)  # Peso inicial en 0
        estado_inicial = nuevo_estado

    return G

def bloquear_nodos_aleatoriamente(G, num_nodos):
    """
    Bloquea nodos aleatoriamente en el grafo.
    
    Args:
    - G: Grafo en el que se bloquearán los nodos.
    - num_nodos: Número de nodos a bloquear.
    
    Returns:
    - G: Grafo con nodos bloqueados.
    """
    nodos = list(G.nodes())
    nodos_bloqueados = random.sample(nodos, num_nodos)
    for nodo in nodos_bloqueados:
        G.remove_node(nodo)
    return G, nodos_bloqueados

def trayectoria_optima(G, estado_inicial, estado_final):
    """
    Calcula la trayectoria óptima desde un estado inicial hasta un estado final en el grafo.
    
    Args:
    - G: Grafo que representa el sistema.
    - estado_inicial: Estado inicial de la partícula (nodo de inicio).
    - estado_final: Estado final de la partícula (nodo de destino).
    
    Returns:
    - path: Lista de nodos que representan la trayectoria óptima.
    """
    try:
        path = nx.dijkstra_path(G, estado_inicial, estado_final, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None

def graficar_grafo_dinamico(G, ruta=None):
    """
    Grafica el grafo de la dinámica de la partícula, mostrando nodos y aristas.
    
    Args:
    - G: Grafo a graficar.
    - ruta: Ruta óptima a resaltar (opcional).
    """
    pos = {n: (n[0], n[1]) for n in G.nodes()}  # Usar posición y velocidad como coordenadas en el gráfico
    labels = {n: f"Pos: {n[0]:.1f}\nVel: {n[1]:.1f}" for n in G.nodes()}  # Etiquetas de posición y velocidad

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, node_size=500, node_color="skyblue", font_size=8, font_weight="bold", arrows=True)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    # Resaltar la ruta óptima si se proporciona
    if ruta:
        ruta_edges = list(zip(ruta, ruta[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=ruta_edges, edge_color="red", width=2)

    plt.xlabel("Posición")
    plt.ylabel("Velocidad")
    plt.title("Simulación de Dinámica de una Partícula: Estados y Transiciones")
    plt.show()

# Crear el grafo de dinámica
grafo_dinamica = crear_grafo_dinamico()

# Definir estados inicial y final
estado_inicial = (0, 0)  # Nodo de inicio
estado_final = (10, 0)  # Nodo de destino

# Bloquear nodos aleatoriamente y buscar el camino más corto
num_nodos_a_bloquear = 2
grafo_dinamica, nodos_bloqueados = bloquear_nodos_aleatoriamente(grafo_dinamica, num_nodos_a_bloquear)
ruta_optima = calcular_camino_mas_corto(grafo_dinamica, estado_inicial, estado_final)

# Graficar el grafo y resaltar la trayectoria óptima
graficar_grafo_dinamico(grafo_dinamica, ruta_optima)
