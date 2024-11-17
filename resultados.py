import tkinter as tk
from tkinter import ttk

def mostrar_metricas(datos_simulacion):
    # Crear la ventana de Tkinter
    ventana = tk.Tk()
    ventana.title("Métricas de la Simulación")

    # Crear el Treeview para mostrar los datos como una tabla
    tabla = ttk.Treeview(ventana, columns=("Paso", "Posición Inicial", "Nueva Posición", "Distancia (m)", 
                                           "Velocidad (m/s)", "Energía Cinética (J)", "Estado", "Tiempo (s)", 
                                           "Distancia Recorrida (m)"), show="headings")

    # Configurar las columnas
    tabla.heading("Paso", text="Paso")
    tabla.heading("Posición Inicial", text="Posición Inicial")
    tabla.heading("Nueva Posición", text="Nueva Posición")
    tabla.heading("Distancia (m)", text="Distancia (m)")
    tabla.heading("Velocidad (m/s)", text="Velocidad (m/s)")
    tabla.heading("Energía Cinética (J)", text="Energía Cinética (J)")
    tabla.heading("Estado", text="Estado")
    tabla.heading("Tiempo (s)", text="Tiempo (s)")
    tabla.heading("Distancia Recorrida (m)", text="Distancia Recorrida (m)")

    # Insertar los datos en la tabla
    for data in datos_simulacion:
        tabla.insert("", "end", values=(data["paso"], data["posicion_inicial"], data["nueva_posicion"], 
                                       round(data["distancia"], 2), round(data["velocidad"], 2), 
                                       round(data["energia_cinetica"], 2), data["Estado"], 
                                       round(data["Tiempo (s)"], 2), round(data["Distancia Recorrida (m)"], 2)))

    # Empacar la tabla
    tabla.pack(fill="both", expand=True)

    # Botón para cerrar la ventana
    btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
    btn_cerrar.pack()

    # Mostrar la ventana
    ventana.mainloop()