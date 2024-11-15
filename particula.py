import random
import time

def simular_dinamica_particula(graph, ruta, velocidad_inicial=0.0, probabilidad_de_parar=0.1, tiempo_de_parada=2):
    """
    Simula la dinámica de una partícula en el grafo.
    
    :param graph: El grafo del hospital.
    :param ruta: La ruta más corta en el grafo.
    :param velocidad_inicial: La velocidad inicial de la partícula.
    :param probabilidad_de_parar: La probabilidad de que la partícula se detenga en cada paso.
    :param tiempo_de_parada: El tiempo que la partícula se detiene antes de reanudar el movimiento.
    :return: El grafo actualizado y los datos de la simulación.
    """
    posicion_inicial = ruta[0]  # Nodo de inicio
    velocidad = round(random.uniform(1.0, 5.0), 3)  # Velocidad aleatoria inicial aproximada a 3 decimales
    datos_simulacion = []

    for paso in range(1, len(ruta)):
        nueva_posicion = ruta[paso]  # Actualizar la posición según la ruta

        # Simular la posibilidad de que la partícula se detenga
        if random.random() < probabilidad_de_parar:
            velocidad = 0  # La partícula se detiene
            time.sleep(tiempo_de_parada)  # Esperar antes de reanudar el movimiento
            velocidad = round(random.uniform(1.0, 5.0), 3)  # Reanudar el movimiento con una nueva velocidad aleatoria aproximada a 3 decimales

        # Asegurarse de que el peso de la arista comience en cero
        if graph.has_edge(posicion_inicial, nueva_posicion):
            data = graph.get_edge_data(posicion_inicial, nueva_posicion)
            data['weight'] = velocidad  # Actualizar el peso con la velocidad

        datos_simulacion.append({
            'paso': paso,
            'posicion_inicial': posicion_inicial,
            'nueva_posicion': nueva_posicion,
            'velocidad': velocidad,
            'mostrar': False  # Agregar un campo para controlar la visualización
        })

        posicion_inicial = nueva_posicion  # Actualizar la posición inicial para el siguiente paso
        time.sleep(1 / velocidad)  # Simular el tiempo de movimiento basado en la velocidad

    return graph, datos_simulacion