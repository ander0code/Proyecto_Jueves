import random
from edificio import Esquema_grafo_hospital

# Función que simula la dinámica de la partícula en el hospital
def simular_dinamica_particula():
    G = Esquema_grafo_hospital()  # Obtener el grafo del hospital
    shortest_path = ["Recepción", "Escaleras 1A", "Emergencias", "Escaleras 1B", "Consultorios", "Escaleras 1C", "Radiología"]
    
    datos_simulacion = []
    velocidad_inicial = 1.0  # Velocidad inicial de la partícula
    probabilidad_de_parar = 0.1  # Probabilidad de que la partícula se detenga en cada paso
    tiempo_de_parada = 2  # Tiempo de parada si la partícula se detiene
    
    # Lógica para simular el movimiento de la partícula a lo largo del camino más corto
    tiempo_total = 0
    distancia_recorrida = 0
    paradas = 0

    for i in range(len(shortest_path) - 1):
        nodo_actual = shortest_path[i]
        nodo_siguiente = shortest_path[i + 1]
        
        # Simular si la partícula se detiene
        if random.random() < probabilidad_de_parar:
            estado = "Inactiva"
            paradas += 1
            tiempo_total += tiempo_de_parada
        else:
            estado = "Activa"
            tiempo_total += 1
        
        distancia_recorrida += 1  # Incrementamos la distancia

        # Guardar los datos de cada paso
        datos_simulacion.append({
            "Paso": i + 1,
            "Nodo Actual": nodo_actual,
            "Velocidad (m/s)": round(velocidad_inicial, 2),
            "Tiempo (s)": round(tiempo_total, 2),
            "Distancia Recorrida (m)": round(distancia_recorrida, 2),
            "Estado": estado,
            "Dirección": f"De {nodo_actual} a {nodo_siguiente}"
        })
    
    return datos_simulacion