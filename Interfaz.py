import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame

#CLASE DE FACCIONES
class Facciones:
    def __init__(self, nombre, fondo_menu, botones, texto_boton):
        self.nombre = nombre
        self.fondo_menu = fondo_menu
        self.botones = botones
        self.texto_boton = texto_boton

# Creamos las 3 instancias de la clase y las guardamos en una lista
lista_facciones = [
    Facciones("Predeterminada", "#D12B4D", "#532B97", "white"),
    Facciones("Futurista", "#0F172A", "#06B6D4", "white"),
    Facciones("Medieval", "#3F2E21", "#3B8336", "black")
]

# Variables globales para rastrear el estado actual
faccion_actual = lista_facciones[0]  # Empieza con la Predeterminada (índice 0)
ventana_actual = None


# Función para cambiar el tema visual buscando el objeto en la lista con un ciclo FOR
# Función para cambiar el tema visual (CORREGIDA)
def cambiar_faccion(nombre_seleccionado):
    global faccion_actual
    
    # Buscamos el objeto facción que coincida con el nombre seleccionado usando un for
    for faccion in lista_facciones:
        if faccion.nombre == nombre_seleccionado:  # <-- CORREGIDO: cambiamos .name por .nombre
            faccion_actual = faccion
            break
            
    # Extraer y aplicar los nuevos colores del objeto encontrado
    main_frame.config(bg=faccion_actual.fondo_menu)
    Boton1.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    Boton2.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    Boton3.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    Boton4.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    boton_cerrar_principal.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    label_faccion.config(bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton)

# Funciones de control de ventanas
def cerrar_root():
    global ventana_actual
    if ventana_actual is not None and ventana_actual.winfo_exists():
        ventana_actual.destroy()
    ventana.deiconify()

def salir_del_juego():
    ventana.destroy()


# Ventana principal (Menú)
ventana = tk.Tk()
ventana.title("Juego Proyecto II")
ventana.geometry("620x520")
ventana.resizable(False, False)

# El fondo inicial se toma del objeto faccion_actual
main_frame = tk.Frame(ventana, bg=faccion_actual.fondo_menu)
main_frame.pack(fill=tk.BOTH, expand=True)


# --- INTERFAZ DEL SELECTOR DE FACCIONES ---
label_faccion = tk.Label(main_frame, text="Seleccionar Facción:", font=("Arial", 10, "bold"),
                         bg=faccion_actual.fondo_menu, fg="white")
label_faccion.place(x=20, y=15)

variable_faccion = tk.StringVar(ventana)
variable_faccion.set(faccion_actual.nombre) # Opción por defecto

# Extraemos solo los nombres para pasárselos al OptionMenu
nombres_facciones = []
for f in lista_facciones:
    nombres_facciones.append(f.nombre)

selector_faccion = tk.OptionMenu(main_frame, variable_faccion, *nombres_facciones, command=cambiar_faccion)
selector_faccion.config(font=("Arial", 10), bg="#FFFFFF")
selector_faccion.place(x=170, y=12)


# Funciones para abrir ventanas secundarias aplicando el objeto faccion_actual activo
def click1():
    global ventana_actual
    ventana.withdraw()
    
    top = tk.Toplevel(ventana)
    top.title("Registro")
    top.geometry("420x280")
    top.config(bg=faccion_actual.fondo_menu) # Aplica el fondo temático
    ventana_actual = top
    
    boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), 
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton, command=cerrar_root)
    boton_cerrado.place(x=385, y=5)
    
    top.protocol("WM_DELETE_WINDOW", cerrar_root)

def click2(): # PARA ABRIR EL JUEGO
    global ventana_actual
    ventana.withdraw()
    
    top = tk.Toplevel(ventana)
    top.title("Juego")
    top.geometry("600x420")
    top.config(bg=faccion_actual.fondo_menu)
    ventana_actual = top
    
    boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), 
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton, command=cerrar_root)
    boton_cerrado.place(x=565, y=5)
    
    top.protocol("WM_DELETE_WINDOW", cerrar_root)

def click3():
    global ventana_actual
    ventana.withdraw()
    
    top = tk.Toplevel(ventana)
    top.title("Puntaje")
    top.geometry("420x280")
    top.config(bg=faccion_actual.fondo_menu)
    ventana_actual = top
    
    boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), 
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton, command=cerrar_root)
    boton_cerrado.place(x=385, y=5)
    
    top.protocol("WM_DELETE_WINDOW", cerrar_root)


# Botones ventana principal

boton_cerrar_principal = tk.Button(main_frame, text='X', font=("Arial", 10, "bold"), #Para cerrar ventana principal
                                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                                   activeforeground="#C3D12B", 
                                   command=salir_del_juego)
boton_cerrar_principal.place(x=585, y=5)

Boton1 = tk.Button(main_frame, text="Registro", command=click1, 
                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                   activebackground="#C3D12B", activeforeground="white",
                   font=("Arial", 12, "bold"), width=24, height=2)
Boton1.place(x=186,y=100)

Boton2 = tk.Button(main_frame, text="JUGAR", command=click2, 
                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                   activebackground="#C3D12B", activeforeground="white",
                   font=("Arial", 12, "bold"), width=24, height=2)
Boton2.place(x=186, y=200)

Boton3 = tk.Button(main_frame, text="Puntajes", command=click3, 
                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                   activebackground="#C3D12B", activeforeground="white",
                   font=("Arial", 12, "bold"), width=24, height=2)
Boton3.place(x=186, y=300)


# BOTÓN MÚSICA
pygame.mixer.init()
musica_activa = False

def alternar_musica():
    global musica_activa
    if not musica_activa:
        pygame.mixer.music.load("mi_cancion.mp3")
        pygame.mixer.music.play(-1)
        Boton4.config(text="Pausar Música")
        musica_activa = True
    else:
        pygame.mixer.music.stop()
        Boton4.config(text="Reproducir Música")
        musica_activa = False

Boton4 = tk.Button(main_frame, text="ON/OFF MUSICA", command=alternar_musica, 
                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
Boton4.place(x=260, y=460)  

ventana.mainloop()