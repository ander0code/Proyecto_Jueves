import tkinter as tk
from tkinter import messagebox
from simulacion import simular_dinamica_particula

def mostrar_resultados():
    datos = simular_dinamica_particula()

    resultado_texto = ""
    for paso in datos:
        resultado_texto += f"Paso {paso['Paso']}: {paso['Nodo Actual']} -> {paso['Dirección']}\n"
        resultado_texto += f"Estado: {paso['Estado']}, Velocidad: {paso['Velocidad (m/s)']} m/s\n"
        resultado_texto += f"Tiempo: {paso['Tiempo (s)']} s, Distancia Recorrida: {paso['Distancia Recorrida (m)']} m\n\n"

    ventana_resultados = tk.Tk()
    ventana_resultados.title("Resultados de la Simulación")
    texto_resultado = tk.Text(ventana_resultados, width=60, height=20)
    texto_resultado.pack()
    texto_resultado.insert(tk.END, resultado_texto)
    ventana_resultados.mainloop()

# Configuración de la interfaz
def interfaz():
    ventana = tk.Tk()
    ventana.title("Simulación de Partícula en Hospital")
    ventana.geometry("400x200")

    boton_simulacion = tk.Button(ventana, text="Iniciar Simulación", command=mostrar_resultados)
    boton_simulacion.pack(pady=20)

    ventana.mainloop()

if __name__ == "__main__":
    interfaz()