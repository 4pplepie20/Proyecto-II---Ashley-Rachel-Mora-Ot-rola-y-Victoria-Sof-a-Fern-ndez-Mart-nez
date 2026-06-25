import time

"ESTADO DE TORRES"
class EstadoTorre: #Sirve para representar 
    def __init__(self, vida):
        self.vida = vida
        self.congelada = False
    
    def recibir_dano(self, dano):
        self.vida -= dano
    
    def congelar(self):
        self.congelada = True

"CLASE BASE DE TORRES"
class Torres:

    'Atributo'
    def __init__(self, nombre, costo, vida, dano, alcance, habilidad): #Todos los datos necesarios sobre las torres
        self.nombre = nombre #Nombre de la torre
        self.costo = costo #Cuántas monedas se necesitan para comprarla
        self.vida = vida #La cantidad de vida predeterminada
        self.dano = dano #El daño que produce a enemigos
        self.alcance = alcance #El alcance de sus ataques
        self.habilidad = habilidad #El número de segundos necesarios para usar la habilidad especial
        self.recarga = 0 #El inicio del turno, empieza en 0
    
    'Métodos'
    def dano_recibido(self, cantidad): #Daño causado a la torre
        self.vida -= cantidad #La vida se resta según la cantidad de daño que causa el enemigo

    def verificación_rango(self, fila_torre, columna_torre, fila_unidad, columna_unidad): #Verifica si un enemigo está lo suficientemente cerca de la torre
        distancia = abs(fila_torre - fila_unidad) + abs(columna_torre - columna_unidad) #Calcula la distancia y se utiliza valor absoluto para evitar números negativos
        
        if distancia <= self.alcance: #Condición de que debe ser una distancia menor o igual al alcance de la torre
            return True #La distancia es menor o igual al alcance de la torre, así que se ataca
        return False #La distancia es mayor, no cumple la condición
    
    def ataque(self, estadotorre): #Daño que ejerce al enemigo
        estadotorre.recibir_dano(self.dano) #Llama a la función que recibe el objetivo
    
    def habilidad_disponible(self): #Función para saber si ya es posible utilizar la habilidad
        tiempo_ahora = time.time() #Ofrece el tiempo actual en segundos

        if tiempo_ahora - self.recarga >= self.habilidad: #Condición de que debe el tiempo debe ser mayor o igual a la cantidad necesaria para activar el poder
            return True #Cumple la condición
        return False #No cumple la condición

    def habilidad_especial(self): #Es solo un molde para las subclases
        pass


"TIPOS DE TORRES"

'TORRE BÁSICA'
class TorreBasica(Torres): #Subclase con el tipo de torre, con el "Torres" dentro del nombre de la clase deja una herencia de información

    'Atributos'
    def __init__(self): 
        super().__init__( #El super(). llama a los atributos de la clase base
            "Torre Básica", #Nombre de la torre
            50, #Costo
            100, #Vida (HP)
            20, #Daño ejercido
            2, #Alcance
            5 #Tiempo de recarga
        )
    
    def habilidad_especial(self, estadotorre): #Habilidad especial de la torre
        if self.habilidad_disponible(): #Condición si ha pasado el tiempo suficiente
            estadotorre.recibir_dano(self.dano) #Hace daño dos veces por el doble disparo
            estadotorre.recibir_dano(self.dano)

            self.recarga = time.time() #Regresa al tiempo pasado

class TorrePesada(Torres): 
    def __init__(self):
        super().__init__(
            "Torre Pesada",
            135,
            200,
            40,
            2,
            12
        )
    
    def habilidad_especial(self, estadotorre):
        if self.habilidad_disponible():
            estadotorre.recibir_dano(self.dano * 2) #El daño se duplica

            self.recarga = time.time()
    
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
    
    def habilidad_especial(self, estadotorre):
        if self.habilidad_disponible():
            estadotorre.congelar() #Llama la función congelar y la vuelve True

            self.recarga = time.time()

"JUGADOR DE DEFENSA"
class Defensor: #Clase que representa a quien defiende
    def __init__(self):
        self.dinero = 300 #Dinero inicial
        self.torres = [] #Lista donde se guardarán las torres que compre
    
    def comprar_torres(self, torre): #Función para poder comprar torres
        if self.dinero >= torre.costo: #Condición que el dinero debe ser igual o mayor al costo de la torre
            self.dinero -= torre.costo #Si se cumple la función, se resta el dinero del jugador con el costo de la torre
            self.torres.append(torre) #Concatenación para guardar torre comprada en la lista

            return True #Sí sucedió la compra
        return False #No cumplió la condición, así que no sucedió la compra
