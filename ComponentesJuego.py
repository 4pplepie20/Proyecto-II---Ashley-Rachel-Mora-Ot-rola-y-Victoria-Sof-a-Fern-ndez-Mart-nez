import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Librerías esenciales para procesar y redimensionar imágenes .png
from Torres import Defensor, TorreBasica, TorrePesada, TorreMagica 

class TableroJuego: # Clase encargada de construir y gestionar el mapa interactivo de casillas
    
    def __init__(self, ventana_contenedor, faccion_defensor, faccion_atacante, defensor_logico): 
        self.contenedor = ventana_contenedor
        self.faccion_defensor = faccion_defensor  # Objeto de la facción elegida por el jugador 1 (Defensor)
        self.faccion_atacante = faccion_atacante  # Objeto de la facción elegida por el jugador 2 (Atacante)
        self.defensor = defensor_logico           # Conexión lógica con Torres.py para manejar dinero y compras
        
        # Matriz lógica de 10x10 que inicia vacía (None) para registrar las estructuras
        self.matriz_logica = [[None for _ in range(10)] for _ in range(10)] 
        self.casillas = []                        # Guardará las referencias visuales de cada botón tk.Button
        
        # Obtiene los colores de fondo del mapa basados en el defensor
        self.color1, self.color2 = self.obtener_colores_faccion()
        
        # --- ATRIBUTOS INDIVIDUALES PARA LAS IMÁGENES PIXEL ART (SIN DICCIONARIOS) ---
        self.imagen_torre_basica = None
        self.imagen_torre_magica = None
        self.imagen_torre_pesada = None
        self.imagen_muro = None
        
        # Método interno para cargar los archivos físicos .png antes de pintar el tablero
        self.cargar_recursos_imagenes()
        
        # Ejecuta la construcción visual de la cuadrícula
        self.generar_tablero()

    def cargar_recursos_imagenes(self):
        """
        Evalúa el nombre de la facción del defensor mediante condicionales directos
        y precarga los archivos de imagen correspondientes redimensionándolos a 60x60 píxeles.
        """
        nombre_facc = self.faccion_defensor.nombre
        
        # Inicializamos las rutas de archivos de forma predeterminada vacías
        archivo_basica = ""
        archivo_magica = ""
        archivo_pesada = ""
        archivo_muro = ""
        
        # Asignación exacta según los nombres estandarizados de las imágenes
        if nombre_facc == "Medieval":
            archivo_basica = "Torrebasicamedieval.png"
            archivo_magica = "Torremagicamedieval.png"
            archivo_pesada = "Torrepesadamedieval.png"
            archivo_muro   = "Muromedieval.png"
            
        elif nombre_facc == "Futurista":
            archivo_basica = "Torrebasicafuturista.png"
            archivo_magica = "TorremMagicafuturista.png"
            archivo_pesada = "Torrepesadafuturista.png"
            archivo_muro   = "Murofuturista.png"
            
        elif nombre_facc == "Zombie":
            archivo_basica = "Torrebasicazombie.png"
            archivo_magica = "Torremagicazombie.png"
            archivo_pesada = "Torrepesadazombie.png"
            archivo_muro   = "Murozombie.png"

        # --- BLOQUES DE CARGA SEGUROS E INDIVIDUALES ---
        # Definimos que cada casilla mida exactamente 60x60 píxeles en pantalla
        TAMANO_SPRITE = (60, 60)
        
        if archivo_basica != "":
            try:
                img = Image.open(archivo_basica).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS)
                self.imagen_torre_basica = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error cargando {archivo_basica}: {e}")

        if archivo_magica != "":
            try:
                img = Image.open(archivo_magica).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS)
                self.imagen_torre_magica = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error cargando {archivo_magica}: {e}")

        if archivo_pesada != "":
            try:
                img = Image.open(archivo_pesada).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS)
                self.imagen_torre_pesada = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error cargando {archivo_pesada}: {e}")

        if archivo_muro != "":
            try:
                img = Image.open(archivo_muro).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS)
                self.imagen_muro = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error cargando {archivo_muro}: {e}")

    def obtener_colores_faccion(self): 
        """
        Establece los dos colores alternados de las casillas según la facción defensora.
        """
        nombre_faccion = self.faccion_defensor.nombre
        if nombre_faccion == "Medieval":
            return "#360857", "#5B1491"
        elif nombre_faccion == "Futurista":
            return "#0F172A", "#1E293B"
        elif nombre_faccion == "Zombie":
            return "#2D3111", "#42471A"
        else:
            return "#FFFFFF", "#000000"

    def casilla_clickeada(self, fila, columna): 
        """
        Maneja la acción de colocar una estructura en la matriz cuando el jugador pulsa una casilla.
        """
        if self.matriz_logica[fila][columna] is not None: 
            torre_existente = self.matriz_logica[fila][columna] 
            messagebox.showinfo("Casilla Ocupada", f"Aquí ya hay una {torre_existente.nombre}.\nVida: {torre_existente.vida}")
            return

        # Instanciamos por defecto una Torre Básica para la prueba de compra
        nueva_torre = TorreBasica() 

        if self.defensor.dinero >= nueva_torre.costo: 
            self.defensor.comprar_torres(nueva_torre)          
            self.matriz_logica[fila][columna] = nueva_torre     
            
            boton_presionado = self.casillas[fila][columna]     
            
            # --- SELECCIÓN Y ASIGNACIÓN DINÁMICA DE IMÁGENES ---
            imagen_a_colocar = None
            emoji_respaldo = "🏰"

            if isinstance(nueva_torre, TorreBasica):
                imagen_a_colocar = self.imagen_torre_basica
                emoji_respaldo = "🏹"
            elif isinstance(nueva_torre, TorreMagica):
                imagen_a_colocar = self.imagen_torre_magica
                emoji_respaldo = "🔮"
            elif isinstance(nueva_torre, TorrePesada):
                imagen_a_colocar = self.imagen_torre_pesada
                emoji_respaldo = "💥"
            
            # Si la imagen correspondiente fue cargada con éxito a memoria, la mostramos
            if imagen_a_colocar is not None:
                boton_presionado.config(image=imagen_a_colocar, text="")
                boton_presionado.image = imagen_a_colocar  # Mantiene la referencia viva en Tkinter
            else:
                # Respaldo visual si no se encuentran las imágenes en la carpeta raíz
                boton_presionado.config(text=emoji_respaldo, fg="white", font=("Arial", 16, "bold"))
            
            print(f"¡{nueva_torre.nombre} colocada en [{fila}, {columna}]!")
            messagebox.showinfo("Compra Exitosa", f"Se colocó {nueva_torre.nombre}.\nDinero restante: ${self.defensor.dinero}") 
        else: 
            messagebox.showwarning("Fondos Insuficientes", 
                                   f"No te alcanza para la {nueva_torre.nombre}.\nCosto: ${nueva_torre.costo}\nTu dinero: ${self.defensor.dinero}")

    def generar_tablero(self): 
        """
        Dibuja físicamente la cuadrícula de botones fijando el tamaño de cada fila 
        y columna en píxeles exactos para evitar colapsos visuales.
        """
        marco_tablero = tk.Frame(self.contenedor, bg=self.faccion_defensor.fondo_menu, bd=2, relief="solid")
        marco_tablero.pack(expand=True, pady=(20, 20)) 

        # Forzamos a que las 10 columnas midan exactamente 60 píxeles de ancho de manera absoluta
        for c in range(10):
            marco_tablero.grid_columnconfigure(c, minsize=60, weight=1)
        # Forzamos a que las 10 filas midan exactamente 60 píxeles de alto de manera absoluta
        for f in range(10):
            marco_tablero.grid_rowconfigure(f, minsize=60, weight=1)

        for fila in range(10):
            fila_botones = []
            for columna in range(10):
                if (fila + columna) % 2 == 0: 
                    color_fondo = self.color1
                else:
                    color_fondo = self.color2
                
                # Creamos el botón vacío sin dimensiones de caracteres de texto fijas
                btn_casilla = tk.Button( 
                    marco_tablero, 
                    bg=color_fondo, 
                    activebackground="#C3D12B", 
                    bd=1, 
                    relief="groove"
                )
                # Al usar sticky="nsew", forzamos al botón a rellenar el espacio absoluto de la celda de 60x60
                btn_casilla.grid(row=fila, column=columna, sticky="nsew")
                
                # Vinculamos la acción de manera segura
                btn_casilla.config(command=lambda f=fila, c=columna: self.casilla_clickeada(f, c))
                
                fila_botones.append(btn_casilla)
                
            self.casillas.append(fila_botones)