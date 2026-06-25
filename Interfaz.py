import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import json
from RegistroyCuenta import RegistroUsuarios
gestor_usuarios = RegistroUsuarios ()

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


# Crea la ventana principal (Menú)
ventana = tk.Tk() 
ventana.title("Juego Proyecto II") # Texto que sale en la barra superior
ventana.geometry("620x520") # Define las dimensiones de la ventana
ventana.resizable(False, False) # Para que no se pueda cambiar el tamaño de la ventana

# El fondo inicial se toma del objeto faccion_actual
main_frame = tk.Frame(ventana, bg=faccion_actual.fondo_menu) # Contenedor que 
                                                              #agrupa los botones para poder cambiarles el color facilmente
main_frame.pack(fill=tk.BOTH, expand=True) # Para que el contenedor cubra el 100% de la pantalla


# Interfaz para facciones
label_faccion = tk.Label(main_frame, text="Seleccionar Facción:", font=("Arial", 10, "bold"), # Etiqueta que indica la seleccion de facciones
                         bg=faccion_actual.fondo_menu, fg="white")
label_faccion.place(x=20, y=15) # Ubicación de la etiqueta en el menú principal

variable_faccion = tk.StringVar(ventana) # Crea un objeto especial de tkinter que almacena el texto seleccionado
variable_faccion.set(faccion_actual.nombre) # Le asigna el valor inicial de medieval

#Pasar los nombres de las facciones
nombres_facciones = [] # Crea una lista vacía 
for f in lista_facciones: # Ciclo que revisa uno por uno los objetos (f) de la lista original
    nombres_facciones.append(f.nombre) # Extra el nombre de los atributos y los inserta en una lista nueva, para el menú desplegable

# Menú desplegable
selector_faccion = tk.OptionMenu(main_frame, variable_faccion, *nombres_facciones, command=cambiar_faccion) # Crea la cajita desplegable
selector_faccion.config(font=("Arial", 10), bg="#FFFFFF") 
selector_faccion.place(x=170, y=12) 


#Funciones para abrir ventanas secundarias y cambio de facción
def click1():#PARA ABRIR EL REGISTRO
    global ventana_actual # Avisa que va a cambiar la variable para ver cual ventana secundaria está activa
    ventana.withdraw() # Para ocultar la ventana principal
    
    top = tk.Toplevel(ventana) # Crea la ventana secundaria "Registro"
    top.title("Registro")
    top.geometry("420x280")
    top.config(bg=faccion_actual.fondo_menu) #Para aplicar la facción
    ventana_actual = top # Guarda la nueva ventana en la variable global, para saber qué pantalla tiene abierta el usuario
    
    boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), # Crea botón de X en la ventana secundaria "Registro"
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton, command=cerrar_root)
    boton_cerrado.place(x=385, y=5)

    # Título de la sección dentro de la ventana
    lbl_titulo = tk.Label(top, text="REGISTRO DE USUARIO", font=("Arial", 14, "bold"),
                          bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton)
    lbl_titulo.place(x=100, y=35)

    # Componentes para ingresar el Usuario
    lbl_usuario = tk.Label(top, text="Usuario:", font=("Arial", 11, "bold"),
                           bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton)
    lbl_usuario.place(x=50, y=100)
    
    ent_usuario = tk.Entry(top, font=("Arial", 11), width=22)
    ent_usuario.place(x=160, y=100)

    # Componentes para ingresar la Contraseña
    lbl_contrasena = tk.Label(top, text="Contraseña:", font=("Arial", 11, "bold"),
                              bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton)
    lbl_contrasena.place(x=50, y=150)
    
    ent_contrasena = tk.Entry(top, font=("Arial", 11), width=22, show="*") 
    ent_contrasena.place(x=160, y=150)

    # Función interna encargada de ejecutar el registro conectando la UI con las clases
    def ejecutar_registro():
        nombre = ent_usuario.get().strip()
        contra = ent_contrasena.get().strip()
        
        if nombre == "" or contra == "":
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return
            
        # Llamada directa al método de tu clase RegistroUsuarios
        exito = gestor_usuarios.crear_usuario(nombre, contra)
        
        if exito:
            messagebox.showinfo("Éxito", f"¡Usuario '{nombre}' registrado correctamente!")
            ent_usuario.delete(0, tk.END) # Limpia la caja de texto
            ent_contrasena.delete(0, tk.END) # Limpia la caja de texto
        else:
            messagebox.showerror("Error", "Este nombre de usuario ya se encuentra registrado.")

    # Botón gráfico para enviar el registro
    btn_registrar = tk.Button(top, text="Registrar Cuenta", font=("Arial", 11, "bold"),
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                              command=ejecutar_registro, width=18, height=1)
    btn_registrar.place(x=130, y=220)
    
    top.protocol("WM_DELETE_WINDOW", cerrar_root) # Para que se ejecute cerrar_root al presionar la X original de la ventana también

def click2(): #PARA ABRIR EL JUEGO
    global ventana_actual # Aviso de cambio de variable para saber cual ventana está activa
    ventana.withdraw() # Oculta la ventana principal
    
    top = tk.Toplevel(ventana) # Crea la ventana secundaria "Juego"
    top.title("Juego")
    top.geometry("600x420")
    top.config(bg=faccion_actual.fondo_menu) #Aplica la faccion elegida
    ventana_actual = top # Para saber cuál pantalla tine abrierta el usuario
    
    boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), # Crea botón X en ventana secundaria "Juego"
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton, command=cerrar_root)
    boton_cerrado.place(x=565, y=5)
    
    top.protocol("WM_DELETE_WINDOW", cerrar_root) # Para que se pueda usar la X principal de la ventana tambien

def click3(): #PARA ABRIR EL PUNTAJE
    global ventana_actual # Para saber cual ventana está activa
    ventana.withdraw() # Oculta la ventana principal
    
    top = tk.Toplevel(ventana) # Crea la ventana secundaria "Puntaje"
    top.title("Puntaje")
    top.geometry("420x280")
    top.config(bg=faccion_actual.fondo_menu) # Aplica la faccion 
    ventana_actual = top # Para saber que pantalla está abierta
    
    boton_cerrado = tk.Button(top, text='X', font=("Arial", 10, "bold"), # Crea boton de X en ventana secundaria "Puntaje"
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton, command=cerrar_root)
    boton_cerrado.place(x=385, y=5)
    
    top.protocol("WM_DELETE_WINDOW", cerrar_root) # Para pode usar la X principal de la ventana


#Botones ventana principal

boton_cerrar_principal = tk.Button(main_frame, text='X', font=("Arial", 10, "bold"), #Para cerrar ventana principal
                                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                                   command=salir_del_juego) # Al darle click, la funcion salir_del_juego se ejecuta
boton_cerrar_principal.place(x=585, y=5)

Boton1 = tk.Button(main_frame, text="Registro", command=click1, # Boton de registro en ventana principal, ejecuta la funcion click 1
                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                   activebackground="#C3D12B", activeforeground="white",
                   font=("Arial", 12, "bold"), width=24, height=2)
Boton1.place(x=186,y=100)

Boton2 = tk.Button(main_frame, text="JUGAR", command=click2, # Boton de jugar en ventana principal, ejecuta la funcion click 2
                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                   activebackground="#C3D12B", activeforeground="white",
                   font=("Arial", 12, "bold"), width=24, height=2)
Boton2.place(x=186, y=200)

Boton3 = tk.Button(main_frame, text="Puntajes", command=click3, # Boton de puntajes en ventana principal, ejecuta la funcion click 3
                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                   activebackground="#C3D12B", activeforeground="white",
                   font=("Arial", 12, "bold"), width=24, height=2)
Boton3.place(x=186, y=300)


#BOTÓN 4 MÚSICA
pygame.mixer.init() #Prepara a la computadora para reproducir la musica

def alternar_musica():  #Evalua el estado booleano de musica_activa
    global musica_activa
    if not musica_activa: # Si la musica está apagada procede a encenderla con try
        try:
            pygame.mixer.music.load(faccion_actual.cancion) # Carga el atributo de la facción seleccionada 
            pygame.mixer.music.play(-1) # Para que la funcion se ejecute de forma infinita
            Boton4.config(text="Pausar Música") # Cambia el texto del botón segun se encienda o apague
            musica_activa = True #Actualiza el estado de la variable
        except pygame.error: #Si hay un error con el archivo mostrará el siguiente mensaje
            messagebox.showerror("Error", f"No se encontró el archivo de sonido: {faccion_actual.cancion}")
    else:
        pygame.mixer.music.stop() # Si la música está activa la apaga
        Boton4.config(text="Reproducir Música") # Cambia el texto del boton 
        musica_activa = False # Cambia el estado de la variable global 

Boton4 = tk.Button(main_frame, text="ON/OFF MUSICA", command=alternar_musica, #Crea el boton de música en la ventana principal
                   bg=faccion_actual.botones, fg=faccion_actual.texto_boton)
Boton4.place(x=260, y=460)  

ventana.mainloop()