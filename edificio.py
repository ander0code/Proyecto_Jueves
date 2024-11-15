import networkx as nx
import matplotlib.pyplot as plt

def Esquema_grafo_hospital():
    G = nx.Graph()  

    # Piso 1
    G.add_node("Recepción", pos=(5, 5), floor=1)
    G.add_node("Escaleras 1A", pos=(20, 5), floor=1)
    G.add_node("Emergencias", pos=(35, 5), floor=1)
    G.add_node("Escaleras 1B", pos=(50, 5), floor=1)
    G.add_node("Consultorios", pos=(65, 5), floor=1)
    G.add_node("Escaleras 1C", pos=(80, 5), floor=1)
    G.add_node("Radiología", pos=(95, 5), floor=1)
    G.add_node("Escaleras 1D", pos=(110, 5), floor=1)

    G.add_edge("Recepción", "Escaleras 1A", weight=0)
    G.add_edge("Escaleras 1A", "Emergencias", weight=0)
    G.add_edge("Emergencias", "Escaleras 1B", weight=0)
    G.add_edge("Escaleras 1B", "Consultorios", weight=0)
    G.add_edge("Consultorios", "Escaleras 1C", weight=0)
    G.add_edge("Escaleras 1C", "Radiología", weight=0)
    G.add_edge("Radiología", "Escaleras 1D", weight=0)
    
    # Piso 2
    G.add_node("Laboratorio", pos=(5, 15), floor=2)
    G.add_node("Escaleras 2A", pos=(20, 15), floor=2)
    G.add_node("Quirófanos", pos=(35, 15), floor=2)
    G.add_node("Escaleras 2B", pos=(50, 15), floor=2)
    G.add_node("UCI", pos=(65, 15), floor=2)
    G.add_node("Escaleras 2C", pos=(80, 15), floor=2)
    G.add_node("Farmacia", pos=(95, 15), floor=2)
    G.add_node("Escaleras 2D", pos=(110, 15), floor=2)

    G.add_edge("Laboratorio", "Escaleras 2A", weight=0)
    G.add_edge("Escaleras 2A", "Quirófanos", weight=0)
    G.add_edge("Quirófanos", "Escaleras 2B", weight=0)
    G.add_edge("Escaleras 2B", "UCI", weight=0)
    G.add_edge("UCI", "Escaleras 2C", weight=0)
    G.add_edge("Escaleras 2C", "Farmacia", weight=0)
    G.add_edge("Farmacia", "Escaleras 2D", weight=0)

    # Piso 3
    G.add_node("Dormitorios", pos=(5, 25), floor=3)
    G.add_node("Escaleras 3A", pos=(20, 25), floor=3)
    G.add_node("Pediatría", pos=(35, 25), floor=3)
    G.add_node("Escaleras 3B", pos=(50, 25), floor=3)
    G.add_node("Ginecología", pos=(65, 25), floor=3)
    G.add_node("Escaleras 3C", pos=(80, 25), floor=3)
    G.add_node("Sala de Espera", pos=(95, 25), floor=3)
    G.add_node("Escaleras 3D", pos=(110, 25), floor=3)

    G.add_edge("Dormitorios", "Escaleras 3A", weight=0)
    G.add_edge("Escaleras 3A", "Pediatría", weight=0)
    G.add_edge("Pediatría", "Escaleras 3B", weight=0)
    G.add_edge("Escaleras 3B", "Ginecología", weight=0)
    G.add_edge("Ginecología", "Escaleras 3C", weight=0)
    G.add_edge("Escaleras 3C", "Sala de Espera", weight=0)
    G.add_edge("Sala de Espera", "Escaleras 3D", weight=0)

    # Conexiones verticales
    G.add_edge("Escaleras 1A", "Escaleras 2A", weight=0)
    G.add_edge("Escaleras 2A", "Escaleras 3A", weight=0)
    G.add_edge("Escaleras 1B", "Escaleras 2B", weight=0)
    G.add_edge("Escaleras 2B", "Escaleras 3B", weight=0)
    G.add_edge("Escaleras 1C", "Escaleras 2C", weight=0)
    G.add_edge("Escaleras 2C", "Escaleras 3C", weight=0)
    G.add_edge("Escaleras 1D", "Escaleras 2D", weight=0)
    G.add_edge("Escaleras 2D", "Escaleras 3D", weight=0)

    return G
