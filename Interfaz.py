import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import json

#CLASE DE FACCIONES
class Facciones: #Molde para crear objetos tipo facción 
    def __init__(self, nombre, fondo_menu, botones, texto_boton, cancion):
        self.nombre = nombre  # guarda características individuales dentro del objeto para que no se pierdan
        self.fondo_menu = fondo_menu
        self.botones = botones
        self.texto_boton = texto_boton
        self.cancion = cancion

#3 instancias de la clase en lista que almacenan las 3 facciones disponibles
lista_facciones = [
    Facciones("Medieval", "#360857", "#88743F", "white", "Medieval.mp3"),
    Facciones("Futurista", "#0F172A", "#06B6D4", "white", "Futurista.mp3"),
    Facciones("Zombie", "#2D3111", "#811818", "white", "Zombie.mp3")
]

#Variables globales para rastrear el estado actual
faccion_actual = lista_facciones[0]  # Define con cuál facción se empieza por defecto, empieza con medieval
ventana_actual = None #Para recordar cuál ventana secundaria está abierta, empieza vacía
musica_activa = False #Si la musica está en ON u Off



#Función para cambiar el tema visual, se activa cuando el usuario elige una opción diferente en el menú de facciones
def cambiar_faccion(nombre_seleccionado):
    global faccion_actual,musica_activa # Avisa que va a cambiar las variables
    for faccion in lista_facciones: # Recorre lista de facciones una por una
        if faccion.nombre == nombre_seleccionado: #Si el nombre de la lista coincide con el seleccionado, guarda el objeto en faccion_actual
            faccion_actual = faccion                 
            break                   #Detiene el ciclo con break
            
    # Extraer y aplicar los nuevos colores
    main_frame.config(bg=faccion_actual.fondo_menu) # Redibuja visualmente el menú principal cada que se cambia de faccion
    Boton1.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    Boton2.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    Boton3.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    Boton4.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    boton_cerrar_principal.config(bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
    label_faccion.config(bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton)


    # 2. Control de cambio de música
    if musica_activa: #Si la musica esta activa, la cambia automáticamente
        try:
            pygame.mixer.music.stop() # Detiene la canción de la facción anterior
            pygame.mixer.music.load(faccion_actual.cancion) # Carga la canción de la nueva facción
            pygame.mixer.music.play(-1) # La reproduce en bucle infinito
        except pygame.error: # Si al cargar el sonido hay un problema con el archivo,
                             # muestra un aviso para evitar que se cierre el juego por completo
            print(f"No se pudo cargar el archivo de audio: {faccion_actual.cancion}")


#Funciones de control de ventanas
def cerrar_root(): # Se ejecuta cuando se pulsa la X de alguna ventana secundaria
    global ventana_actual
    if ventana_actual is not None and ventana_actual.winfo_exists(): # Verifica si la ventana secundaria está abierta
        ventana_actual.destroy() # Cierra la ventana abierta
    ventana.deiconify() # Hace que la ventana del menú principal reaparezca

def salir_del_juego(): # Se ejecuta al presionar la X del menú primcipal
    ventana.destroy() # Cierra por completo el juego


# Ventana principal (Menú)
ventana = tk.Tk()
ventana.title("Juego Proyecto II")
ventana.geometry("620x520")
ventana.resizable(False, False)

# El fondo inicial se toma del objeto faccion_actual
main_frame = tk.Frame(ventana, bg=faccion_actual.fondo_menu)
main_frame.pack(fill=tk.BOTH, expand=True)


# Interfaz para facciones
label_faccion = tk.Label(main_frame, text="Seleccionar Facción:", font=("Arial", 10, "bold"),
                         bg=faccion_actual.fondo_menu, fg="white")
label_faccion.place(x=20, y=15)

variable_faccion = tk.StringVar(ventana)
variable_faccion.set(faccion_actual.nombre) #Opción por defecto

#Pasar los nombres al OptionMenu
nombres_facciones = []
for f in lista_facciones:
    nombres_facciones.append(f.nombre)

selector_faccion = tk.OptionMenu(main_frame, variable_faccion, *nombres_facciones, command=cambiar_faccion)
selector_faccion.config(font=("Arial", 10), bg="#FFFFFF")
selector_faccion.place(x=170, y=12)


#Funciones para abrir ventanas secundarias con facción
def click1():#PARA ABRIR EL REGISTRO
    global ventana_actual
    ventana.withdraw()
    
    top = tk.Toplevel(ventana)
    top.title("Registro")
    top.geometry("420x280")
    top.config(bg=faccion_actual.fondo_menu) #Para aplicar la facción
    ventana_actual = top
    
    boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), 
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton, command=cerrar_root)
    boton_cerrado.place(x=385, y=5)
    
    top.protocol("WM_DELETE_WINDOW", cerrar_root)

def click2(): #PARA ABRIR EL JUEGO
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

def click3(): #PARA ABRIR EL PUNTAJE
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


#Botones ventana principal

boton_cerrar_principal = tk.Button(main_frame, text='X', font=("Arial", 10, "bold"), #Para cerrar ventana principal
                                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
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


#BOTÓN MÚSICA
pygame.mixer.init()

def alternar_musica():
    global musica_activa
    if not musica_activa:
        try:
            pygame.mixer.music.load(faccion_actual.cancion)
            pygame.mixer.music.play(-1)
            Boton4.config(text="Pausar Música")
            musica_activa = True
        except pygame.error:
            messagebox.showerror("Error", f"No se encontró el archivo de sonido: {faccion_actual.cancion}")
    else:
        pygame.mixer.music.stop()
        Boton4.config(text="Reproducir Música")
        musica_activa = False

Boton4 = tk.Button(main_frame, text="ON/OFF MUSICA", command=alternar_musica, 
                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
Boton4.place(x=260, y=460)  

ventana.mainloop()