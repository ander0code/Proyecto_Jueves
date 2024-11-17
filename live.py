from resultados import mostrar_metricas
import networkx as nx
import matplotlib.pyplot as plt
from edificio import Esquema_grafo_hospital  
from particula import simular_dinamica_particula  
import tkinter as tk  
import random
from camino_mas_corto import calcular_camino_mas_corto  
import matplotlib.animation as animation 
from simulacion import simular_dinamica_particula

def recalibrate_graph(graph, nodos_bloqueados):
    print("Recalibrando el grafo y buscando el camino más corto...")
    shortest_path = calcular_camino_mas_corto(graph, "Sala de Espera", "Recepción")
    datos_simulacion = []
    if shortest_path:

        for u, v, data in graph.edges(data=True):
            data['weight'] = 0
        graph, datos_simulacion = simular_dinamica_particula(
            graph, 
            shortest_path, 
            velocidad_inicial=0.0, 
            probabilidad_de_parar=0.1, 
            tiempo_de_parada=2
        )
    return graph, shortest_path, datos_simulacion

def introducir_obstaculos(graph, probabilidad_de_obstaculo=0.1):

    for nodo in list(graph.nodes()):
        if random.random() < probabilidad_de_obstaculo and nodo != "Recepción":  
            graph.remove_node(nodo)
    return graph

def plot_graph(graph, ax, shortest_path=None, datos_simulacion=None):
    pos = nx.get_node_attributes(graph, 'pos')
    ax.clear()  
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
    plt.draw() 
    plt.pause(0.1)  

def bloquear_nodos(graph, nodos_bloqueados):
    for nodo in nodos_bloqueados:
        if nodo in graph and nodo != "Recepción":  
            graph.remove_node(nodo)
    return graph

def desbloquear_nodos(graph, nodos_desbloqueados, posiciones_originales):
    for nodo in nodos_desbloqueados:
        if nodo not in graph:
            graph.add_node(nodo, pos=posiciones_originales[nodo])
    return graph

def bloquear_nodos_aleatoriamente(graph, num_nodos, camino):

    nodos = list(graph.nodes())
    if "Recepción" in nodos:
        nodos.remove("Recepción")  
    
    nodos_bloqueables = [nodo for nodo in nodos if nodo not in camino]
    
    nodos_bloqueados = random.sample(nodos_bloqueables, num_nodos) 
    
    for nodo in nodos_bloqueados:
        graph.nodes[nodo]['color'] = 'orange' 
    
    return graph, nodos_bloqueados

def actualizar_grafico(num, graph, ax, camino, datos_simulacion):

    ax.clear()
    pos = nx.get_node_attributes(graph, 'pos')

    node_colors = [graph.nodes[nodo].get('color', 'lightblue') for nodo in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color=node_colors, font_size=10, font_weight='bold', ax=ax)
    
    edge_labels = {}
    for datos in datos_simulacion:
        if datos['paso'] <= num:
            edge_labels[(datos['posicion_inicial'], datos['nueva_posicion'])] = datos['velocidad']
            datos['mostrar'] = True  
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
    
    path_edges = list(zip(camino, camino[1:]))
    
    if num >= len(camino) - 1:
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)
        ax.set_title("El camino completo ha sido recorrido - Todo en rojo")
    else:
        end_index = num + 2 
        if end_index < len(camino):
            path_edges_to_paint = list(zip(camino[num:end_index], camino[num+1:end_index+1]))
        else:
            path_edges_to_paint = list(zip(camino[num:], camino[num+1:])) 

        nx.draw_networkx_edges(graph, pos, edgelist=path_edges_to_paint, edge_color='red', width=2)

        nodo_actual = camino[num]
        nx.draw_networkx_nodes(graph, pos, nodelist=[nodo_actual], node_color='red', node_size=3000, ax=ax)

    plt.draw()  
    plt.pause(0.1)  

def simular_movimiento(graph, camino, ax, datos_simulacion):
    anim = animation.FuncAnimation(
        plt.gcf(),
        actualizar_grafico,
        frames=len(camino) + 1,  
        fargs=(graph, ax, camino, datos_simulacion),
        interval=2000,
        repeat=False
    )
    plt.show(block=True) 
    return anim  
def main():
    plt.ion()  
    fig, ax = plt.subplots(figsize=(15, 10))

    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.withdraw()  

    window_width = 15 * 100  
    window_height = 10 * 100  
    position_x = (screen_width - window_width) // 2
    position_y = (screen_height - window_height) // 2


    fig.canvas.manager.window.wm_geometry(f"+{position_x}+{position_y}")

    graph = Esquema_grafo_hospital()  


    posiciones_originales = nx.get_node_attributes(graph, 'pos')

    nodos_bloqueados = [] 

    graph, shortest_path, datos_simulacion = recalibrate_graph(graph, nodos_bloqueados)
    if shortest_path:
        print(f"Camino más corto: {shortest_path}")

        num_nodos_a_bloquear = 5
        graph, nodos_bloqueados = bloquear_nodos_aleatoriamente(graph, num_nodos_a_bloquear, shortest_path)

        anim = simular_movimiento(graph, shortest_path, ax, datos_simulacion) 
        

        if datos_simulacion:
            mostrar_metricas(datos_simulacion)

if __name__ == "__main__":
    main()

