import threading
import time
import networkx as nx
import matplotlib.pyplot as plt
from edificio import Esquema_grafo_hospital  # Importar el grafo del hospital
from particula import simular_dinamica_particula  # Importar la simulación de la partícula
import tkinter as tk  # Importar tkinter para obtener la resolución de la pantalla
import random
from camino_mas_corto import calcular_camino_mas_corto  # Importar la función para calcular el camino más corto
from tkinter import ttk  # Importar ttk para widgets de tkinter
import matplotlib.animation as animation  # Importar para la animación

def recalibrate_graph(graph, nodos_bloqueados):
    print("Recalibrando el grafo y buscando el camino más corto...")
    shortest_path = calcular_camino_mas_corto(graph, "Sala de Espera", "Recepción")
    datos_simulacion = []
    if shortest_path:
        # Asegurarse de que todos los pesos de las aristas comiencen en cero
        for u, v, data in graph.edges(data=True):
            data['weight'] = 0
        graph, datos_simulacion = simular_dinamica_particula(graph, shortest_path, velocidad_inicial=0.0, probabilidad_de_parar=0.1, tiempo_de_parada=2)
    return graph, shortest_path, datos_simulacion

def introducir_obstaculos(graph, probabilidad_de_obstaculo=0.1):
    """
    Introduce obstáculos aleatorios en el grafo.
    
    :param graph: El grafo del hospital.
    :param probabilidad_de_obstaculo: La probabilidad de que un nodo se bloquee temporalmente.
    :return: El grafo actualizado.
    """
    for nodo in list(graph.nodes()):
        if random.random() < probabilidad_de_obstaculo and nodo != "Recepción":  # No eliminar el nodo "Recepción"
            graph.remove_node(nodo)
    return graph

def plot_graph(graph, ax, shortest_path=None, datos_simulacion=None):
    pos = nx.get_node_attributes(graph, 'pos')
    ax.clear()  # Limpiar el gráfico anterior
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', ax=ax)
    
    if datos_simulacion:
        edge_labels = {}
        for datos in datos_simulacion:
            if datos['mostrar']:
                edge_labels[(datos['posicion_inicial'], datos['nueva_posicion'])] = datos['velocidad']
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
    
    if shortest_path:
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)
    
    ax.set_title("Esquema del Grafo del Hospital")
    plt.draw()  # Dibujar el gráfico actualizado
    plt.pause(0.1)  # Pausar brevemente para permitir la actualización

def bloquear_nodos(graph, nodos_bloqueados):
    for nodo in nodos_bloqueados:
        if nodo in graph and nodo != "Recepción":  # No eliminar el nodo "Recepción"
            graph.remove_node(nodo)
    return graph

def desbloquear_nodos(graph, nodos_desbloqueados, posiciones_originales):
    for nodo in nodos_desbloqueados:
        if nodo not in graph:
            graph.add_node(nodo, pos=posiciones_originales[nodo])
    return graph

def bloquear_nodos_aleatoriamente(graph, num_nodos):
    nodos = list(graph.nodes())
    if "Recepción" in nodos:
        nodos.remove("Recepción")  # Asegurarse de que "Recepción" no sea bloqueado
    nodos_bloqueados = random.sample(nodos, num_nodos)
    for nodo in nodos_bloqueados:
        graph.remove_node(nodo)
    return graph, nodos_bloqueados

def actualizar_grafico(num, graph, ax, camino, datos_simulacion):
    ax.clear()
    pos = nx.get_node_attributes(graph, 'pos')
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', ax=ax)
    
    edge_labels = {}
    for datos in datos_simulacion:
        if datos['paso'] <= num:
            edge_labels[(datos['posicion_inicial'], datos['nueva_posicion'])] = datos['velocidad']
            datos['mostrar'] = True  # Mostrar la velocidad después de que el punto rojo haya pasado
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
    
    path_edges = list(zip(camino, camino[1:]))
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)
    
    nodo_actual = camino[num]
    nx.draw_networkx_nodes(graph, pos, nodelist=[nodo_actual], node_color='red', node_size=3000, ax=ax)
    ax.set_title(f"Esquema del Grafo del Hospital - Paso {num+1}")

def simular_movimiento(graph, camino, ax, datos_simulacion):
    anim = animation.FuncAnimation(plt.gcf(), actualizar_grafico, frames=len(camino), fargs=(graph, ax, camino, datos_simulacion), interval=2000, repeat=False)  # Intervalo de 2000 ms (2 segundos)
    plt.show(block=True)  # Mantener el gráfico abierto
    return anim  # Retornar la animación para que no sea eliminada

def main():
    plt.ion()  # Habilitar modo interactivo
    fig, ax = plt.subplots(figsize=(15, 10))

    # Definir root antes de usarlo
    root = tk.Tk()
    # Obtener la resolución de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.withdraw()  # Ocultar la ventana de tkinter

    # Calcular la posición para centrar la ventana
    window_width = 15 * 100  # Ancho de la ventana en píxeles
    window_height = 10 * 100  # Alto de la ventana en píxeles
    position_x = (screen_width - window_width) // 2
    position_y = (screen_height - window_height) // 2

    # Ajustar la posición de la ventana de Matplotlib
    fig.canvas.manager.window.wm_geometry(f"+{position_x}+{position_y}")

    graph = Esquema_grafo_hospital()  # Crear el grafo del hospital

    # Guardar las posiciones originales de los nodos
    posiciones_originales = nx.get_node_attributes(graph, 'pos')

    # Bloquear nodos aleatoriamente
    num_nodos_a_bloquear = 2
    graph, nodos_bloqueados = bloquear_nodos_aleatoriamente(graph, num_nodos_a_bloquear)

    # Recalibrar el grafo y buscar el camino más corto en el hilo principal
    graph, shortest_path, datos_simulacion = recalibrate_graph(graph, nodos_bloqueados)
    if shortest_path:
        print(f"Camino más corto: {shortest_path}")
        anim = simular_movimiento(graph, shortest_path, ax, datos_simulacion)  # Simular el movimiento a lo largo del camino más corto

if __name__ == "__main__":
    main()