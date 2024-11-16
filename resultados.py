import tkinter as tk
from tkinter import ttk

def mostrar_metricas(datos_simulacion):
    """
    Muestra una ventana con las métricas y datos generados durante la simulación.
    
    :param datos_simulacion: Lista de diccionarios con los datos de la simulación.
    """
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Resultados de la Dinámica de la Partícula")
    ventana.geometry("800x400")  # Ajustar tamaño de la ventana
    
    # Crear el frame para la tabla
    frame = ttk.Frame(ventana)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Crear un árbol para mostrar las métricas
    columnas = ("paso", "posicion_inicial", "nueva_posicion", "distancia", "velocidad", "energia_cinetica")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings")
    
    # Configurar encabezados
    tabla.heading("paso", text="Paso")
    tabla.heading("posicion_inicial", text="Nodo Inicial")
    tabla.heading("nueva_posicion", text="Nodo Final")
    tabla.heading("distancia", text="Distancia")
    tabla.heading("velocidad", text="Velocidad")
    tabla.heading("energia_cinetica", text="Energía Cinética")
    
    # Configurar tamaños de columnas
    tabla.column("paso", width=50)
    tabla.column("posicion_inicial", width=100)
    tabla.column("nueva_posicion", width=100)
    tabla.column("distancia", width=100)
    tabla.column("velocidad", width=100)
    tabla.column("energia_cinetica", width=120)
    
    # Insertar los datos de la simulación en la tabla
    for datos in datos_simulacion:
        tabla.insert("", tk.END, values=(
            datos["paso"],
            datos["posicion_inicial"],
            datos["nueva_posicion"],
            round(datos["distancia"], 3),
            datos["velocidad"],
            round(datos["energia_cinetica"], 3),
        ))
    
    # Añadir scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tabla.pack(fill=tk.BOTH, expand=True)
    
    # Botón para cerrar la ventana
    boton_cerrar = ttk.Button(ventana, text="Cerrar", command=ventana.destroy)
    boton_cerrar.pack(pady=10)
    
    # Ejecutar la ventana
    ventana.mainloop()
