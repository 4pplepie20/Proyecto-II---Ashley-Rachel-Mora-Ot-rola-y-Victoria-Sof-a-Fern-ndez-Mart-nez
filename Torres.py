import time

"CLASE BASE DE TORRES"
class Torres:

    'Atributo'
    def __init__(self, nombre, costo, vida, dano, alcance, habilidad): #Todos los datos necesarios sobre las torres
        self.nombre = nombre #Nombre de la torre
        self.costo = costo #Cuántas monedas se necesitan para comprarla
        self.vida = vida #La cantidad de vida predeterminada
        self.dano = dano #El daño que produce a enemigos
        self.alcance = alcance #El alcance de sus ataques (casillas de distancia)
        self.habilidad = habilidad #El número de segundos necesarios para usar la habilidad especial
        self.recarga = 0 #El inicio del turno, empieza en 0
        # Posición en el tablero que se asigna al comprarse
        self.fila = 0
        self.columna = 0
    
    'Métodos'
    def dano_recibido(self, cantidad): #Daño causado a la torre por un atacante
        self.vida -= cantidad 
    
    def recibir_dano(self, cantidad): # Nombre alterno por compatibilidad con Combate.py
        self.vida -= cantidad

    def destruida(self): # Evalúa si la torre cayó
        return self.vida <= 0

    # CORRECCIÓN: Método vital para realizar el daño al atacante
    def ataque(self, enemigo):
        if hasattr(enemigo, "dano_recibido"):
            enemigo.dano_recibido(self.dano)

    # CORRECCIÓN: Método que solicita Combate.py para saber si el atacante está en rango
    def verificacion_rango(self, unidad):
        # Si la torre es un Muro, no ataca a nadie (rango falso)
        if "Muro" in self.nombre:
            return False
            
        # Verifica si el atacante está en la misma columna y dentro del alcance (hacia abajo)
        if self.columna == unidad.columna and unidad.fila > self.fila:
            distancia = unidad.fila - self.fila
            if distancia <= self.alcance:
                return True
        return False
        
    def habilidad_disponible(self): #Evalúa si ya pasó el tiempo de recarga
        tiempo_actual = time.time()
        if tiempo_actual - self.recarga >= self.habilidad:
            return True
        return False
    
    def usar_habilidad(self): #Establece el tiempo en el que se usó la habilidad
        self.recarga = time.time()
        
    def habilidad_especial(self, enemigo):
        pass


"CLASES DE LAS TORRES INDIVIDUALES"

class TorreBasica(Torres):
    def __init__(self):
        super().__init__(
            "Torre Básica",
            50,
            100,
            15,
            2,
            4
        )
        
    def habilidad_especial(self, enemigo):
        if self.habilidad_disponible():
            # CORRECCIÓN: Se envía el daño como argumento y se usa dano_recibido
            if hasattr(enemigo, "dano_recibido"):
                enemigo.dano_recibido(self.dano * 2) # El daño se duplica
            self.usar_habilidad()
    
class TorrePesada(Torres):
    def __init__(self):
        super().__init__(
            "Torre Pesada",
            120,
            150,
            40,
            1,
            6
        )
        
    def habilidad_especial(self, enemigo):
        if self.habilidad_disponible():
            if hasattr(enemigo, "dano_recibido"):
                enemigo.dano_recibido(self.dano * 2) # El daño se duplica
            self.usar_habilidad()
    
class TorreMagica(Torres):
    def __init__(self):
        super().__init__(
            "Torre Mágica",
            75,
            75,
            10,
            3,
            5
        )
    
    def habilidad_especial(self, enemigo):
        if self.habilidad_disponible():
            # CORRECCIÓN: Si el atacante tiene la propiedad de congelarse o recibir efectos
            if hasattr(enemigo, "congelar"):
                enemigo.congelar() 
            elif hasattr(enemigo, "dano_recibido"):
                # Como alternativa, si no hay estado de congelación programado en el atacante, le resta velocidad temporalmente o hace daño
                enemigo.dano_recibido(self.dano)
            self.usar_habilidad()


"JUGADOR DE DEFENSA"
class Defensor: #Clase que representa a quien defiende
    def __init__(self):
        self.dinero = 300 #Dinero inicial
        self.torres = [] #Lista donde se guardarán las torres que compre
    
    def comprar_torres(self, torres): #Función para poder comprar torres
        if self.dinero >= torres.costo: 
            self.dinero -= torres.costo 
            self.torres.append(torres) 
            return True 
        return False