import time #Biblioteca que consigue el tiempo

"ESTADO DEL ATACANTE"
class EstadoAtacante: #Clase que verifica cuál es el estado del atacante

    'Atributos'
    def __init__(self, vida): #__init__ es para asignar atributos dentro de la clase
        self.vida = vida #Vida que posee el atacante
        self.escudo = False

    'Métodos'    
    def recibir_dano(self, dano): #Función para evaluar el daño recibido
        self.vida -= dano #Se le resta a la vida el daño que se ha recibido
    
    def activar_escudo(self):
        self.escudo = True

"CLASE BASE DE LOS ATACANTES"
class Atacante: #Clase que funciona como molde para la función de los atacantes

    'Atributos'
    def __init__(self, nombre, costo, vida, dano, velocidad, habilidad): #Datos a conocer de cada uno de los atacantes
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.dano = dano
        self.velocidad = velocidad
        self.habilidad = habilidad
        self.recarga = 0
        # CORRECCIÓN: Atributos de posición inicializados por defecto
        self.fila = 0
        self.columna = 0
        self.ultimo_movimiento = time.time() # Para controlar la fluidez de movimiento
        self.ultimo_ataque = time.time()     # Para controlar la fluidez de ataque
    
    'Métodos'
    def dano_recibido(self, cantidad): #Función que indica la cantidad de daño causado hacia el atacante
        self.vida -= cantidad #Cálculo entre la cantidad de vida del atacante menos la cantidad de vida que quita
    
    def destruida(self):
        return self.vida <= 0

    def mover(self, fila_actual):
        fila_actual += self.velocidad
        return fila_actual
    
    def ataque(self, objetivo):
        objetivo.recibir_dano(self.dano)
    
    def habilidad_disponible(self):
        tiempo_actual = time.time()
        if tiempo_actual - self.recarga >= self.habilidad:
            return True
        return False
    
    def usar_habilidad(self):
        self.recarga = time.time()

    def habilidad_especial(self, objetivo):
        pass

class SoldadoBasico(Atacante):
    def __init__(self):
        super().__init__(
            "Soldado Básico",
            40,
            100,
            20,
            1, # 1 casilla por segundo
            5
        )
    
    def habilidad_especial(self, objetivo):
        if self.habilidad_disponible():
            objetivo.recibir_dano(self.dano)
            objetivo.recibir_dano(self.dano)
            self.usar_habilidad()
        
class Tanque(Atacante):
    def __init__(self):
        super().__init__(
            "Tanque",
            90,
            250,
            35,
            0.5, # Más lento: 1 casilla cada 2 segundos
            8
        )
    
    def habilidad_especial(self, objetivo):
        if self.habilidad_disponible():
            # CORRECCIÓN: Cambiado 'recibir_daño' por 'recibir_dano' para evitar errores
            objetivo.recibir_dano(self.dano * 2)
            self.usar_habilidad()

class Explorador(Atacante):
    def __init__(self):
        super().__init__(
            "Explorador",
            70,
            80, 
            15,
            2, # Más rápido: 2 casillas por segundo
            4
        )
    def habilidad_especial(self, estadoatacante):
        if self.habilidad_disponible():
            if hasattr(estadoatacante, 'activar_escudo'):
                estadoatacante.activar_escudo()
            self.usar_habilidad()

class RolAtacante:
    def __init__(self):
        self.dinero = 500
        self.atacantes = []
    
    def comprar_atacante(self, atacante):
        if self.dinero >= atacante.costo:
            self.dinero -= atacante.costo
            self.atacantes.append(atacante)
            return True
        return False
    
    def ganar_dinero(self, ganancias):
        self.dinero += ganancias