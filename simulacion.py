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

    pos = nx.get_node_attributes(graph, 'pos')  
    distancia_recorrida_total = 0  # Variable para acumular la distancia total recorrida
    tiempo_total = 0  # Variable para acumular el tiempo total

    for paso in range(1, len(ruta)):
        nueva_posicion = ruta[paso]
        distancia = calcular_distancia(posicion_inicial, nueva_posicion, pos)
        
        # Actualiza la distancia total recorrida
        distancia_recorrida_total += distancia
        
        # Calcular la velocidad aleatoria
        velocidad = round(random.uniform(1.0, 5.0), 3)
        
        # Calcular el tiempo para este paso
        tiempo = distancia / velocidad
        tiempo_total += tiempo
        
        # Calcular la energía cinética
        energia_cinetica = 0.5 * masa * (velocidad**2)

        # Determinar si la partícula se detiene por un tiempo debido a la probabilidad de parada
        if random.random() < probabilidad_de_parar:
            estado = "Inactiva"  # Se detiene
            velocidad = 0  # La partícula se detiene
            time.sleep(tiempo_de_parada)  # Pausa por tiempo_de_parada
            velocidad = round(random.uniform(1.0, 5.0), 3)  # Reinicia la velocidad
        else:
            estado = "Activa"  # Sigue en movimiento

        # Añadir los datos al registro de la simulación
        datos_simulacion.append({
            'paso': paso,
            'posicion_inicial': posicion_inicial,
            'nueva_posicion': nueva_posicion,
            'distancia': distancia,
            'velocidad': velocidad,
            'energia_cinetica': energia_cinetica,
            'mostrar': False,
            'Estado': estado,  # Aquí se agrega la clave 'Estado'
            'Tiempo (s)': round(tiempo_total, 2),  # Tiempo acumulado en segundos
            'Distancia Recorrida (m)': round(distancia_recorrida_total, 2),  # Distancia total recorrida
        })
        
        # Actualizar la posición para el siguiente paso
        posicion_inicial = nueva_posicion
        time.sleep(1 / velocidad)  # Retraso en el movimiento de la partícula
        
    return graph, datos_simulacion