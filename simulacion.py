import math
import random
import time
import networkx as nx

def calcular_distancia(nodo1, nodo2, pos):
    x1, y1 = pos[nodo1]
    x2, y2 = pos[nodo2]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def simular_dinamica_particula(graph, ruta, velocidad_inicial=0.0, probabilidad_de_parar=0.1, tiempo_de_parada=2, masa=1.0):
    posicion_inicial = ruta[0]
    velocidad = velocidad_inicial
    datos_simulacion = []

    pos = nx.get_node_attributes(graph, 'pos')  # Obtener posiciones para cálculo de distancias

    for paso in range(1, len(ruta)):
        nueva_posicion = ruta[paso]
        distancia = calcular_distancia(posicion_inicial, nueva_posicion, pos)
        
        # Asignar velocidad aleatoria y calcular tiempo
        velocidad = round(random.uniform(1.0, 5.0), 3)
        tiempo = distancia / velocidad

        # Calcular energía cinética
        energia_cinetica = 0.5 * masa * (velocidad**2)

        # Simular probabilidad de detenerse
        if random.random() < probabilidad_de_parar:
            velocidad = 0  # Detenerse
            time.sleep(tiempo_de_parada)
            velocidad = round(random.uniform(1.0, 5.0), 3)  # Reanudar movimiento

        # Actualizar el peso de la arista
        if graph.has_edge(posicion_inicial, nueva_posicion):
            data = graph.get_edge_data(posicion_inicial, nueva_posicion)
            data['weight'] = velocidad  # Actualizar peso como velocidad

        datos_simulacion.append({
            'paso': paso,
            'posicion_inicial': posicion_inicial,
            'nueva_posicion': nueva_posicion,
            'distancia': distancia,
            'velocidad': velocidad,
            'energia_cinetica': energia_cinetica,
            'mostrar': False
        })

        posicion_inicial = nueva_posicion
        time.sleep(1 / velocidad)  # Simular tiempo de movimiento

    return graph, datos_simulacion