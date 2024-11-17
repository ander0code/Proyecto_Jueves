import networkx as nx
import matplotlib.pyplot as plt
import random
from camino_mas_corto import calcular_camino_mas_corto
def crear_grafo_dinamico():

    G = nx.DiGraph()  

    posicion_inicial = 0
    velocidad_inicial = 0  
    estado_inicial = (posicion_inicial, velocidad_inicial)
    G.add_node(estado_inicial)

    for paso in range(1, 11): 
        nueva_posicion = paso
        nuevo_estado = (nueva_posicion, velocidad_inicial)
        G.add_node(nuevo_estado)
        G.add_edge(estado_inicial, nuevo_estado, weight=0) 
        estado_inicial = nuevo_estado

    return G

def bloquear_nodos_aleatoriamente(G, num_nodos):

    nodos = list(G.nodes())
    nodos_bloqueados = random.sample(nodos, num_nodos)
    for nodo in nodos_bloqueados:
        G.remove_node(nodo)
    return G, nodos_bloqueados

def trayectoria_optima(G, estado_inicial, estado_final):

    try:
        path = nx.dijkstra_path(G, estado_inicial, estado_final, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None

def graficar_grafo_dinamico(G, ruta=None):

    pos = {n: (n[0], n[1]) for n in G.nodes()}  
    labels = {n: f"Pos: {n[0]:.1f}\nVel: {n[1]:.1f}" for n in G.nodes()}  

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, node_size=500, node_color="skyblue", font_size=8, font_weight="bold", arrows=True)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    if ruta:
        ruta_edges = list(zip(ruta, ruta[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=ruta_edges, edge_color="red", width=2)

    plt.xlabel("Posición")
    plt.ylabel("Velocidad")
    plt.title("Simulación de Dinámica de una Partícula: Estados y Transiciones")
    plt.show()

grafo_dinamica = crear_grafo_dinamico()

estado_inicial = (0, 0) 
estado_final = (10, 0) 

num_nodos_a_bloquear = 2
grafo_dinamica, nodos_bloqueados = bloquear_nodos_aleatoriamente(grafo_dinamica, num_nodos_a_bloquear)
ruta_optima = calcular_camino_mas_corto(grafo_dinamica, estado_inicial, estado_final)

graficar_grafo_dinamico(grafo_dinamica, ruta_optima)
