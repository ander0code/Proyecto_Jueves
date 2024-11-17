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
from playsound import playsound
from gtts import gTTS
import os
import threading
from pydub import AudioSegment

def crear_audio_guia(shortest_path):
    # Definir los nombres de los archivos de audio
    audio_path = "guia.mp3"
    audio_rapido_path = "guia_rápida.mp3"

    # Eliminar archivos existentes si ya existen
    for file_path in [audio_path, audio_rapido_path]:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo eliminado: {file_path}")

    # Crear un texto optimizado para las instrucciones
    texto_guia = "Siga estas indicaciones: "
    for i in range(len(shortest_path) - 1):
        texto_guia += f"{shortest_path[i]} a {shortest_path[i+1]}. "
    texto_guia += f"Llegada final en {shortest_path[-1]}. Gracias por usar nuestro sistema de guía."

    # Crear el audio usando gTTS
    audio = gTTS(text=texto_guia, lang="es")
    audio.save(audio_path)

    # Usar pydub para modificar la velocidad del audio
    audio = AudioSegment.from_mp3(audio_path)
    audio_rapido = audio.speedup(playback_speed=1.2)  # Incremento del 30%
    audio_rapido.export(audio_rapido_path, format="mp3")

    print("El archivo de audio rápido 'guia_rápida.mp3' se ha creado correctamente.")
    return audio_rapido_path

def reproducir_audio_guia():
    audio_path = os.path.abspath("guia_rápida.mp3")  

    try:
        print(f"Reproduciendo el archivo: {audio_path}")
        playsound(audio_path)  
    except Exception as e:
        print(f"Error al reproducir el audio: {e}")

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
    hilo_audio = threading.Thread(target=reproducir_audio_guia)  # Ajustado para usar guia_rápida.mp3
    hilo_audio.start()

    anim = animation.FuncAnimation(
        plt.gcf(),
        actualizar_grafico,
        frames=len(camino) + 1,
        fargs=(graph, ax, camino, datos_simulacion),
        interval=2000,
        repeat=False
    )
    plt.show(block=True) 
    hilo_audio.join()
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
        crear_audio_guia(shortest_path) 

        num_nodos_a_bloquear = 5 
        graph, nodos_bloqueados = bloquear_nodos_aleatoriamente(graph, num_nodos_a_bloquear, shortest_path)

        anim = simular_movimiento(graph, shortest_path, ax, datos_simulacion) 
        
        if datos_simulacion:
            mostrar_metricas(datos_simulacion)

if __name__ == "__main__":
    main()