import random
import time

def simular_dinamica_particula(graph, ruta, velocidad_inicial=0.0, probabilidad_de_parar=0.1, tiempo_de_parada=2):

    posicion_inicial = ruta[0] 
    velocidad = round(random.uniform(1.0, 5.0), 3) 
    datos_simulacion = []

    for paso in range(1, len(ruta)):
        nueva_posicion = ruta[paso] 

        if random.random() < probabilidad_de_parar:
            velocidad = 0  
            time.sleep(tiempo_de_parada)  
            velocidad = round(random.uniform(1.0, 5.0), 3) 

        if graph.has_edge(posicion_inicial, nueva_posicion):
            data = graph.get_edge_data(posicion_inicial, nueva_posicion)
            data['weight'] = velocidad  

        datos_simulacion.append({
            'paso': paso,
            'posicion_inicial': posicion_inicial,
            'nueva_posicion': nueva_posicion,
            'velocidad': velocidad,
            'mostrar': False 
        })

        posicion_inicial = nueva_posicion  
        time.sleep(1 / velocidad)  

    return graph, datos_simulacion