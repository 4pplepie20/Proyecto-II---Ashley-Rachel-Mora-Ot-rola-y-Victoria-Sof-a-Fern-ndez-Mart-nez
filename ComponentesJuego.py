import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
from Torres import TorreBasica, TorrePesada, TorreMagica # Asegúrate de importar tu clase Muro aquí si es necesario
from Atacante import SoldadoBasico, Tanque, Explorador
from Juego import Juego 

class TableroJuego:
    def __init__(self, ventana_contenedor, faccion_defensor, faccion_atacante, defensor_logico): 
        self.contenedor = ventana_contenedor
        self.faccion_defensor = faccion_defensor  
        self.faccion_atacante = faccion_atacante  
        
        from Atacante import RolAtacante
        atacante_logico = RolAtacante()
        
        self.juego = Juego(defensor_logico, atacante_logico)
        self.casillas = []                        
        self.def_c1, self.def_c2 = self.obtener_colores_faccion(self.faccion_defensor.nombre)
        self.ata_c1, self.ata_c2 = self.obtener_colores_faccion(self.faccion_atacante.nombre)
        
        self.seleccion_defensor = tk.StringVar(value="Torre Basica")
        self.seleccion_atacante = tk.StringVar(value="Soldado Basico")
        
        # Atributos de imágenes para torres, bases y MUROS
        self.imagen_torre_basica = None
        self.imagen_torre_magica = None
        self.imagen_torre_pesada = None
        self.imagen_muro = None
        self.imagen_base_defensor = None

        # Atributos de imágenes para atacantes
        self.imagen_soldado = None
        self.imagen_tanque = None
        self.imagen_explorador = None
        
        self.cargar_recursos_imagenes()
        
        # --- MENÚS DE COMPRA ARRIBA Y ABAJO ---
        self.menu_superior = tk.Frame(self.contenedor, bg="#1A1A1A", bd=2, relief="raised")
        self.menu_superior.pack(fill="x", side="top", ipady=5)
        
        self.marco_tablero = tk.Frame(self.contenedor, bg="#000000", bd=3, relief="solid")
        self.marco_tablero.pack(expand=True, pady=10)
        
        self.menu_inferior = tk.Frame(self.contenedor, bg="#1A1A1A", bd=2, relief="raised")
        self.menu_inferior.pack(fill="x", side="bottom", ipady=5)
        
        self.construir_menu_defensor()
        self.generar_tablero()
        self.construir_menu_atacante()
        
        messagebox.showinfo("¡PARTIDA INICIADA!", "¡Que empiece el juego!\nEl defensor protege la fila 0. El atacante despliega tropas en la mitad inferior.")
        
        self.juego.iniciar_ronda()
        self.actualizar_renderizado_mapa()
        
        self.bucle_tiempo_real()

    def obtener_colores_faccion(self, nombre_faccion): 
        if nombre_faccion == "Medieval": return "#360857", "#5B1491"
        elif nombre_faccion == "Futurista": return "#0F172A", "#1E293B"
        elif nombre_faccion == "Zombie": return "#2D3111", "#42471A"
        return "#404040", "#262626"

    def cargar_recursos_imagenes(self):
        TAMANO_SPRITE = (40, 40)
        facc_def = self.faccion_defensor.nombre
        facc_ata = self.faccion_atacante.nombre

        # Carga de imágenes de estructuras defensoras (con condicionales, sin diccionarios)
        ruta_tb, ruta_tm, ruta_tp, ruta_muro, ruta_base = "", "", "", "", ""
        if facc_def == "Medieval":
            ruta_tb = "Torrebasicamedieval.png"
            ruta_tm = "Torremagicamedieval.png"
            ruta_tp = "Torrepesadamedieval.png"
            ruta_muro = "Muromedieval.png"
            ruta_base = "Basemedieval.png"
        elif facc_def == "Futurista":
            ruta_tb = "Torrebasicafuturista.png"
            ruta_tm = "TorremMagicafuturista.png"
            ruta_tp = "Torrepesadafuturista.png"
            ruta_muro = "Murofuturista.png"
            ruta_base = "Basefuturista.png"
        elif facc_def == "Zombie":
            ruta_tb = "Torrebasicazombie.png"
            ruta_tm = "Torremagicazombie.png"
            ruta_tp = "Torrepesadazombie.png"
            ruta_muro = "Murozombie.png"
            ruta_base = "Basezombie.png"

        try:
            if ruta_tb != "": self.imagen_torre_basica = ImageTk.PhotoImage(Image.open(ruta_tb).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS))
            if ruta_tm != "": self.imagen_torre_magica = ImageTk.PhotoImage(Image.open(ruta_tm).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS))
            if ruta_tp != "": self.imagen_torre_pesada = ImageTk.PhotoImage(Image.open(ruta_tp).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS))
            if ruta_muro != "": self.imagen_muro = ImageTk.PhotoImage(Image.open(ruta_muro).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS))
            if ruta_base != "": self.imagen_base_defensor = ImageTk.PhotoImage(Image.open(ruta_base).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS))
        except:
            pass

        # Carga de imágenes de atacantes
        ruta_soldado, ruta_tanque, ruta_explorador = "", "", ""
        if facc_ata == "Medieval":
            ruta_soldado = "SoldadoMedieval.png"
            ruta_tanque = "TanqueMedieval.png"
            ruta_explorador = "ExploradorMedieval.png"
        elif facc_ata == "Futurista":
            ruta_soldado = "SoldadoFuturista.png"
            ruta_tanque = "TanqueFuturista.png"
            ruta_explorador = "ExploradorFuturista.png"
        elif facc_ata == "Zombie":
            ruta_soldado = "SoldadoZombie.png"
            ruta_tanque = "TanqueZombie.png"
            ruta_explorador = "ExploradorZombie.png"

        try:
            if ruta_soldado != "": self.imagen_soldado = ImageTk.PhotoImage(Image.open(ruta_soldado).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS))
            if ruta_tanque != "": self.imagen_tanque = ImageTk.PhotoImage(Image.open(ruta_tanque).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS))
            if ruta_explorador != "": self.imagen_explorador = ImageTk.PhotoImage(Image.open(ruta_explorador).resize(TAMANO_SPRITE, Image.Resampling.LANCZOS))
        except:
            pass

    def construir_menu_defensor(self):
        self.lbl_def_info = tk.Label(self.menu_superior, text="", font=("Arial", 11, "bold"), bg="#1A1A1A", fg="#A855F7")
        self.lbl_def_info.pack(side="left", padx=15)
        
        opciones_frame = tk.Frame(self.menu_superior, bg="#1A1A1A")
        opciones_frame.pack(side="right", padx=15)
        
        # Agregamos la opción visual del Muro en la interfaz de compra
        estructuras = [
            ("Torre Básica ($50)", "Torre Basica"), 
            ("Torre Mágica ($100)", "Torre Magica"), 
            ("Torre Pesada ($150)", "Torre Pesada"),
            ("Muro Defensivo ($30)", "Muro")
        ]
        for texto, valor in estructuras:
            tk.Radiobutton(opciones_frame, text=texto, variable=self.seleccion_defensor, value=valor, 
                           bg="#1A1A1A", fg="white", selectcolor="#2D3748", font=("Arial", 9)).pack(side="left", padx=5)

    def construir_menu_atacante(self):
        self.lbl_ata_info = tk.Label(self.menu_inferior, text="", font=("Arial", 11, "bold"), bg="#1A1A1A", fg="#22C55E")
        self.lbl_ata_info.pack(side="left", padx=15)
        
        opciones_frame = tk.Frame(self.menu_inferior, bg="#1A1A1A")
        opciones_frame.pack(side="right", padx=15)
        
        unidades = [("Soldado ($40)", "Soldado Basico"), ("Explorador ($60)", "Explorador"), ("Tanque ($120)", "Tanque")]
        for texto, valor in unidades:
            tk.Radiobutton(opciones_frame, text=texto, variable=self.seleccion_atacante, value=valor, 
                           bg="#1A1A1A", fg="white", selectcolor="#2D3748", font=("Arial", 9)).pack(side="left", padx=5)

    def generar_tablero(self): 
        for c in range(10): self.marco_tablero.grid_columnconfigure(c, minsize=40, weight=1)
        for f in range(10): self.marco_tablero.grid_rowconfigure(f, minsize=40, weight=1)

        for fila in range(10):
            fila_botones = []
            for columna in range(10):
                if fila <= 4:
                    color_fondo = self.def_c1 if (fila + columna) % 2 == 0 else self.def_c2
                else:
                    color_fondo = self.ata_c1 if (fila + columna) % 2 == 0 else self.ata_c2
                
                btn_casilla = tk.Button(self.marco_tablero, bg=color_fondo, activebackground="#C3D12B", bd=1, relief="groove")
                btn_casilla.grid(row=fila, column=columna, sticky="nsew")
                btn_casilla.config(command=lambda f=fila, c=columna: self.casilla_clickeada(f, c))
                fila_botones.append(btn_casilla)
            self.casillas.append(fila_botones)

    def casilla_clickeada(self, fila, columna): 
        if fila == 0:
            messagebox.showwarning("Inválido", "No puedes construir sobre las estructuras de la base principal.")
            return

        if fila <= 4:
            tipo = self.seleccion_defensor.get()
            # Lógica de compra e instanciación del Muro
            if tipo == "Torre Basica": nueva = TorreBasica()
            elif tipo == "Torre Magica": nueva = TorreMagica()
            elif tipo == "Torre Pesada": nueva = TorrePesada()
            else:
                # Aquí instancian su clase Muro desde Torres.py.
                # Si aún no la crean, usaremos TorreBasica temporalmente cambiando su nombre
                from Torres import TorreBasica
                nueva = TorreBasica()
                nueva.nombre = "Muro"
                nueva.costo = 30
                nueva.vida = 300 # Un muro suele tener bastante vida
            
            self.juego.comprar_torre(nueva, fila, columna)
        else:
            tipo = self.seleccion_atacante.get()
            nueva = SoldadoBasico() if tipo == "Soldado Basico" else (Explorador() if tipo == "Explorador" else Tanque())
            self.juego.comprar_unidad(nueva, fila, columna)
        
        self.actualizar_renderizado_mapa()

    def actualizar_renderizado_mapa(self):
        for fila in range(10):
            for columna in range(10):
                casilla = self.casillas[fila][columna]
                entidad_encontrada = None
                tipo_entidad = ""

                for t in self.juego.defensor.torres:
                    if t.fila == fila and t.columna == columna:
                        entidad_encontrada = t
                        tipo_entidad = "TORRE"
                        break
                
                if entidad_encontrada is None:
                    for u in self.juego.rolatacante.atacantes:
                        if u.fila == fila and u.columna == columna:
                            entidad_encontrada = u
                            tipo_entidad = "ATACANTE"
                            break

                if entidad_encontrada is not None:
                    if tipo_entidad == "TORRE":
                        if fila == 0:
                            if self.imagen_base_defensor:
                                if casilla.cget("image") == "":
                                    casilla.config(image=self.imagen_base_defensor, text="")
                                    casilla.image = self.imagen_base_defensor
                            else:
                                casilla.config(text="🏠", fg="#EAB308", font=("Arial", 11, "bold"), image="")
                        else:
                            # Mapea dinámicamente si es torre o un muro
                            self.colocar_grafico_torre(fila, columna, entidad_encontrada.nombre)
                    
                    elif tipo_entidad == "ATACANTE":
                        self.colocar_grafico_atacante(fila, columna, entidad_encontrada)
                else:
                    if fila <= 4:
                        color_original = self.def_c1 if (fila + columna) % 2 == 0 else self.def_c2
                    else:
                        color_original = self.ata_c1 if (fila + columna) % 2 == 0 else self.ata_c2
                    
                    if casilla.cget("text") != "" or casilla.cget("image") != "":
                        casilla.config(image="", text="", bg=color_original)
                        casilla.image = None

        self.actualizar_pantallas_estado()

    def colocar_grafico_torre(self, fila, columna, nombre):
        boton = self.casillas[fila][columna]
        imagen = None
        emoji_respaldo = "🏰"
        
        # Identifica si la estructura es una torre común o es un Muro
        if "Básica" in nombre: imagen = self.imagen_torre_basica
        elif "Mágica" in nombre: imagen = self.imagen_torre_magica
        elif "Pesada" in nombre: imagen = self.imagen_torre_pesada
        elif "Muro" in nombre: 
            imagen = self.imagen_muro
            emoji_respaldo = "🧱" # Icono de ladrillos si no carga la imagen

        if imagen:
            if boton.cget("image") == "":
                boton.config(image=imagen, text="")
                boton.image = imagen
        else:
            boton.config(text=emoji_respaldo, fg="white", font=("Arial", 11, "bold"), image="")

    def colocar_grafico_atacante(self, fila, columna, unidad):
        boton = self.casillas[fila][columna]
        imagen = None
        
        if "Soldado" in unidad.nombre: imagen = self.imagen_soldado
        elif "Tanque" in unidad.nombre: imagen = self.imagen_tanque
        elif "Explorador" in unidad.nombre: imagen = self.imagen_explorador

        if imagen:
            boton.config(image=imagen, text=f"{int(unidad.vida)}", compound="bottom", fg="white", font=("Arial", 8, "bold"))
            boton.image = imagen
        else:
            boton.config(image="", text=f"🧟\n{int(unidad.vida)}", fg="#E11D48", font=("Arial", 8, "bold"))

    def actualizar_pantallas_estado(self):
        total_segundos = self.juego.obtener_tiempo_restante()
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        texto_timer = f"{minutos:02d}:{segundos:02d}"

        self.lbl_def_info.config(
            text=f"DEFENSOR ({self.faccion_defensor.nombre})   |   Dinero: ${self.juego.defensor.dinero}   |   Ronda: {self.juego.ronda}/3   |   Tiempo: {texto_timer}"
        )
        self.lbl_ata_info.config(
            text=f"ATACANTE ({self.faccion_atacante.nombre})   |   Dinero: ${self.juego.rolatacante.dinero}   |   Tiempo: {texto_timer}"
        )

    def bucle_tiempo_real(self):
        self.juego.generar_ingreso_pasivo()
        self.juego.actualizar_ciclo_combate()
        self.actualizar_renderizado_mapa()
        
        if self.juego.atacante_gana_ronda():
            messagebox.showinfo("Ronda Concluida", "¡Una estructura base superior fue destruida! Punto para el Atacante.")
            self.avanzar_ronda_o_terminar()
        elif self.juego.defensor_gana_ronda():
            messagebox.showinfo("Ronda Concluida", "¡El tiempo terminó y resististe la horda! Punto para el Defensor.")
            self.avanzar_ronda_o_terminar()
        else:
            self.contenedor.after(200, self.bucle_tiempo_real)

    def avanzar_ronda_o_terminar(self):
        ganador = self.juego.ganador_final()
        if ganador:
            messagebox.showinfo("¡FIN DE LA PARTIDA!", f"La horda ha terminado.\n¡EL GANADOR ABSOLUTO ES EL {ganador.upper()}!")
            self.contenedor.quit()
        else:
            self.juego.ronda += 1
            self.juego.iniciar_ronda()
            self.actualizar_renderizado_mapa()
            self.bucle_tiempo_real()