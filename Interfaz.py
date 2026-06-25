import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import json
from RegistroyCuenta import RegistroUsuarios
from Puntajes import LogicaPuntajes
gestor_usuarios = RegistroUsuarios ()
controlador_puntajes = LogicaPuntajes(gestor_usuarios) 

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


#Funciones para abrir ventanas secundarias
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

    
    lbl_titulo = tk.Label(top, text="REGISTRO DE USUARIO", font=("Arial", 14, "bold"), # Enunciado dentro de la ventana con etiqueta
                          bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton) # de fondo se escoge las características de la faccion actual
    lbl_titulo.place(x=100, y=35)

    
    lbl_usuario = tk.Label(top, text="Usuario:", font=("Arial", 11, "bold"), # Etiqueta que indica donde ingresar el usuario
                           bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton) # fondo de la faccion actual
    lbl_usuario.place(x=50, y=100)
    
    ent_usuario = tk.Entry(top, font=("Arial", 11), width=22) # Para ingresar el usuario
    ent_usuario.place(x=160, y=100)

    # Componentes para ingresar la Contraseña
    lbl_contrasena = tk.Label(top, text="Contraseña:", font=("Arial", 11, "bold"), # Etiqueta que indica donde ingresar la contraseña
                              bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton)# temática de la facción seleccionada
    lbl_contrasena.place(x=50, y=150)
    
    ent_contrasena = tk.Entry(top, font=("Arial", 11), width=22, show="*") # Para ingresar la contraseña, show=** hace que censure la contraseña
    ent_contrasena.place(x=160, y=150)

    # Función interna encargada de ejecutar el registro conectando la interfaz con las clases
    def ejecutar_registro():
        nombre = ent_usuario.get().strip()
        contra = ent_contrasena.get().strip()
        
        if nombre == "" or contra == "": # Si el usario no ingresa nada sale un mensaje para que complete el campo
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return
            
        exito = gestor_usuarios.crear_usuario(nombre, contra) # Llamada directa al método de la clase RegistroUsuarios
        
        if exito: # Si el usuario logra registrarse sale un mensaje de comprobación
            messagebox.showinfo("Éxito", f"¡Usuario '{nombre}' registrado correctamente!") 
            ent_usuario.delete(0, tk.END) # Limpia la caja de texto
            ent_contrasena.delete(0, tk.END) # Limpia la caja de texto
        else:
            messagebox.showerror("Error", "Este nombre de usuario ya se encuentra registrado.") # Si el usuario pone un nombre ya registrado sale un mensaje de advertencia

    # Boton para registrar cuenta
    btn_registrar = tk.Button(top, text="Registrar Cuenta", font=("Arial", 11, "bold"),
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                              command=ejecutar_registro, width=18, height=1)# Al presionar el boton se ejecuta la funcion ejecutar_registro
    btn_registrar.place(x=130, y=200)

    btn_ir_a_login = tk.Button(top, text="¿Ya tienes cuenta? Inicia Sesión", font=("Arial", 10, "underline"), # Botón para iniciar sesion si ya el usuario tiene una cuenta
                                 bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton,
                                 activebackground=faccion_actual.fondo_menu, activeforeground="gray",
                                 bd=0, command=abrir_login) # Ejecuta la función de abajo
    btn_ir_a_login.place(x=115, y=235)
    
    top.protocol("WM_DELETE_WINDOW", cerrar_root) # Para que se ejecute cerrar_root al presionar la X original de la ventana también

def abrir_login():
    global ventana_actual # Variable que se va a cambiar en la funcion
    
    # Si la ventana de registro estaba abierta (que lo está), la destruimos primero
    if ventana_actual is not None and ventana_actual.winfo_exists(): 
        ventana_actual.destroy()
        
    # Se crea la subventana de Login que sale de la ventana registro
    top_login = tk.Toplevel(ventana)
    top_login.title("Iniciar Sesión")
    top_login.geometry("420x330")
    top_login.config(bg=faccion_actual.fondo_menu) # El fondo es la faccion seleccionada
    ventana_actual = top_login # Reasigna la ventana activa actual
    
    # Botón de X para cerrar la ventana Iniciar Sesion
    boton_cerrado = tk.Button(top_login, text='X', font=("Arial", 10, "bold"), 
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton, command=cerrar_root)# Al presionar el boton se ejecuta cerrar_root
    boton_cerrado.place(x=385, y=5)

    lbl_titulo = tk.Label(top_login, text="INICIO DE SESIÓN", font=("Arial", 14, "bold"), # Etiqueta de la ventana inicio de sesion
                          bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton) # el fondo el la faccion actual
    lbl_titulo.place(x=130, y=35)

    lbl_usuario = tk.Label(top_login, text="Usuario:", font=("Arial", 11, "bold"), # Etiqueta que indica donde poner el usuario
                           bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton) 
    lbl_usuario.place(x=50, y=100)
    
    ent_usuario = tk.Entry(top_login, font=("Arial", 11), width=22) # Espacio para ingresar el usuario
    ent_usuario.place(x=160, y=100)

    lbl_contrasena = tk.Label(top_login, text="Contraseña:", font=("Arial", 11, "bold"), # Etiqueta que indica donde ingresar la contraseña
                              bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton)
    lbl_contrasena.place(x=50, y=150)
    
    ent_contrasena = tk.Entry(top_login, font=("Arial", 11), width=22, show="*") # Espacio para ingresar la contraseña, el show ="*" censura la contraseña
    ent_contrasena.place(x=160, y=150)

    # Ejecución de la validación del Login
    def ejecutar_login():
        nombre = ent_usuario.get().strip() # Extrae el texto ingresado
        contra = ent_contrasena.get().strip() # Extrae el texto ingresado
        
        if nombre == "" or contra == "": # si lee un str vacío muestra mensaje de error para que se complete el campo
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")
            return
        usuario_logeado = gestor_usuarios.iniciar_sesion(nombre, contra) # llama al método iniciar_sesion del objeto global gestor_usuarios y le pasa los datos recolectados
        
        if usuario_logeado is not None: # Si el login fue exitoso
            messagebox.showinfo("Éxito", f"¡Bienvenido de vuelta, {usuario_logeado.obtener_nombre()}!") #Mostrar mensaje
            # Al logearse con éxito, cerramos la subventana y volvemos al menú principal
            cerrar_root() 
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.") # si algo falla, mostrar emnsaje de error

    # Botón para ingresar
    btn_ingresar = tk.Button(top_login, text="Ingresar", font=("Arial", 11, "bold"),
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton,
                              command=ejecutar_login, width=18, height=1) #El boton corre la funcion ejecutar_login
    btn_ingresar.place(x=120, y=210)
    
    # Botón para regresar al registro si cambió de opinión
    btn_volver_registro = tk.Button(top_login, text="¿No tienes cuenta? Regístrate", font=("Arial", 10, "underline"),# texto para el que no tiene cuenta
                                     bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton, # fonfo es la faccion actual
                                     activebackground=faccion_actual.fondo_menu, activeforeground="gray",
                                     bd=0, command=click1) # El boton corre la funcion click1
    btn_volver_registro.place(x=115, y=270)
    top_login.protocol("WM_DELETE_WINDOW", cerrar_root)


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
    
    top_puntajes = tk.Toplevel(ventana) # Crea la ventana secundaria "Puntaje"
    top_puntajes.title("Ranking de Puntajes")
    top_puntajes.geometry("450x400")
    top_puntajes.config(bg=faccion_actual.fondo_menu) # Aplica la faccion 
    ventana_actual = top_puntajes # Para saber que pantalla está abierta
    
    boton_cerrado = tk.Button(top_puntajes, text='X', font=("Arial", 10, "bold"), # Crea boton de X en ventana secundaria "Puntaje"
                              bg=faccion_actual.botones, fg=faccion_actual.texto_boton, command=cerrar_root)
    boton_cerrado.place(x=385, y=5)

    # Título Principal
    lbl_titulo = tk.Label(top_puntajes, text="PUNTAJES Y RANKINGS", font=("Arial", 14, "bold"),
                          bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton)
    lbl_titulo.place(x=110, y=40)
    
    lbl_subtitulo = tk.Label(top_puntajes, text="Selecciona la categoría que deseas visualizar:", font=("Arial", 10, "italic"),
                             bg=faccion_actual.fondo_menu, fg="gray")
    lbl_subtitulo.place(x=90, y=80)

    # Función interna para mostrar el desglose individual de un jugador al darle click a su nombre
    def mostrar_detalles(usuario_objeto):
        nombre = usuario_objeto.obtener_nombre()
        atacante = usuario_objeto.obtener_victorias_atacante()
        defensor = usuario_objeto.obtener_victorias_defensor()
        total = atacante + defensor
        
        mensaje = (f"Usuario: {nombre}\n\n"
                   f"⚔️ Victorias Atacante: {atacante}\n"
                   f"🛡️ Victorias Defensor: {defensor}\n\n"
                   f"⭐ Puntaje Total: {total}")
        messagebox.showinfo("Detalles del Jugador", mensaje)

    # Función interna genérica que construye las subventanas de las listas
    def abrir_sub_ranking(titulo_categoria, lista_ordenada, tipo_puntos):
        top_puntajes.withdraw()
        # Creamos la sub-subventana del ranking específico
        sub_top = tk.Toplevel(top_puntajes)
        sub_top.title(f"Ranking - {titulo_categoria}")
        sub_top.geometry("450x400")
        sub_top.config(bg=faccion_actual.fondo_menu)
        
        # Botón para cerrar ÚNICAMENTE esta subventana y regresar al menú de puntajes
        btn_regresar = tk.Button(sub_top, text='X', font=("Arial", 10, "bold"), 
                                 bg=faccion_actual.botones, fg=faccion_actual.texto_boton, 
                                 command=cerrar_root)
        btn_regresar.place(x=415, y=5)
        
        lbl_tit_sub = tk.Label(sub_top, text=titulo_categoria, font=("Arial", 14, "bold"),
                               bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton)
        lbl_tit_sub.place(x=130, y=30)
        
        lbl_ayuda = tk.Label(sub_top, text="(Haz click en el nombre para ver su historial completo)", font=("Arial", 9, "italic"),
                             bg=faccion_actual.fondo_menu, fg="gray")
        lbl_ayuda.place(x=80, y=60)

        coordenada_y = 110
        posicion = 1
        
        if not lista_ordenada:
            lbl_vacio = tk.Label(sub_top, text="No hay registros disponibles.", font=("Arial", 11),
                                 bg=faccion_actual.fondo_menu, fg="white")
            lbl_vacio.place(x=130, y=160)
            
        for usuario in lista_ordenada:
            # Selecciona qué puntaje imprimir a la par del nombre según el botón oprimido
            if tipo_puntos == "general":
                puntos = usuario.obtener_victorias_atacante() + usuario.obtener_victorias_defensor()
            elif tipo_puntos == "atacante":
                puntos = usuario.obtener_victorias_atacante()
            else:
                puntos = usuario.obtener_victorias_defensor()
                
            texto_puesto = f"{posicion}º  -   Puntos: {puntos}"
            lbl_puesto = tk.Label(sub_top, text=texto_puesto, font=("Arial", 11),
                                  bg=faccion_actual.fondo_menu, fg="white")
            lbl_puesto.place(x=240, y=coordenada_y)

            btn_nombre = tk.Button(sub_top, text=usuario.obtener_nombre(), font=("Arial", 11, "bold", "underline"),
                                   bg=faccion_actual.fondo_menu, fg=faccion_actual.texto_boton,
                                   activebackground=faccion_actual.fondo_menu, activeforeground="gray",
                                   bd=0, command=lambda u=usuario: mostrar_detalles(u))
            btn_nombre.place(x=60, y=coordenada_y)

            coordenada_y += 40
            posicion += 1
            if posicion > 6:
                break

    # --- BOTONES DE SELECCIÓN EN EL MENÚ DE PUNTAJES ---
    
    # 1. Botón para Ranking General
    btn_general = tk.Button(top_puntajes, text="🏆 Ranking General", font=("Arial", 12, "bold"),
                            bg=faccion_actual.botones, fg=faccion_actual.texto_boton, width=25, height=2,
                            command=lambda: abrir_sub_ranking("RANKING GENERAL", controlador_puntajes.obtener_ranking_general(), "general"))
    btn_general.place(x=100, y=140)

    # 2. Botón para Ranking Atacante
    btn_atacante = tk.Button(top_puntajes, text="⚔️ Ranking Atacantes", font=("Arial", 12, "bold"),
                             bg=faccion_actual.botones, fg=faccion_actual.texto_boton, width=25, height=2,
                             command=lambda: abrir_sub_ranking("RANKING ATACANTES", controlador_puntajes.obtener_ranking_atacante(), "atacante"))
    btn_atacante.place(x=100, y=210)

    # 3. Botón para Ranking Defensor
    btn_defensor = tk.Button(top_puntajes, text="🛡️ Ranking Defensores", font=("Arial", 12, "bold"),
                             bg=faccion_actual.botones, fg=faccion_actual.texto_boton, width=25, height=2,
                             command=lambda: abrir_sub_ranking("RANKING DEFENSORES", controlador_puntajes.obtener_ranking_defensor(), "defensor"))
    btn_defensor.place(x=100, y=280)

    top_puntajes.protocol("WM_DELETE_WINDOW", cerrar_root)

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