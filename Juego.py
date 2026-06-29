import time
from Combate import Combate

class EstructuraBaseFija:
    def __init__(self):
        self.nombre = "Base Principal"
        self.costo = 0
        self.vida = 500  
        self.fila = 0
        self.columna = 0

    def destruida(self):
        return self.vida <= 0

    def recibir_dano(self, cantidad):
        self.vida -= cantidad

    def verificacion_rango(self, unidad):
        return False

class Juego:
    def __init__(self, defensor, rolatacante):
        self.defensor = defensor
        self.rolatacante = rolatacante
        self.victorias_defensor = 0
        self.victorias_atacante = 0
        self.ronda = 1
        self.tiempo_ronda = 180  
        self.inicio_ronda = None
        self.filas = 10
        self.columnas = 10
        self.pelea = None
        self.ultimo_ingreso_pasivo = 0 

    def iniciar_ronda(self):
        self.inicio_ronda = time.time()
        self.ultimo_ingreso_pasivo = time.time()
        
        self.defensor.dinero = 300 
        self.rolatacante.dinero = 500
        
        self.defensor.torres = []
        self.rolatacante.atacantes = []
        
        for col in range(self.columnas):
            base_defensora = EstructuraBaseFija()
            base_defensora.fila = 0
            base_defensora.columna = col
            self.defensor.torres.append(base_defensora)
            
        self.pelea = Combate(self.defensor, self.rolatacante)

    def obtener_tiempo_restante(self):
        if self.inicio_ronda is None:
            return self.tiempo_ronda
        tiempo_transcurrido = time.time() - self.inicio_ronda
        restante = self.tiempo_ronda - tiempo_transcurrido
        return max(0, int(restante))

    def tiempo_terminado(self):
        return self.obtener_tiempo_restante() <= 0
    
    def posicion_valida_defensor(self, fila):
        return 1 <= fila <= 4
    
    def posicion_valida_atacante(self, fila):
        return 5 <= fila <= 9
    
    def casilla_ocupada(self, fila, columna):
        for t in self.defensor.torres:
            if t.fila == fila and t.columna == columna:
                return True
        return False
    
    def comprar_torre(self, torres, fila, columna):
        if columna < 0 or columna >= self.columnas:
            return False
        if not self.posicion_valida_defensor(fila) or self.casilla_ocupada(fila, columna):
            return False
        
        if self.defensor.dinero >= torres.costo:
            self.defensor.dinero -= torres.costo
            torres.fila = fila
            torres.columna = columna
            self.defensor.torres.append(torres)
            return True 
        return False
        
    def comprar_unidad(self, unidad, fila, columna):
        if columna < 0 or columna >= self.columnas:
            return False
        if not self.posicion_valida_atacante(fila):
            return False
        
        if self.rolatacante.dinero >= unidad.costo:
            self.rolatacante.dinero -= unidad.costo
            unidad.fila = fila
            unidad.columna = columna
            unidad.ultimo_movimiento = time.time() 
            self.rolatacante.atacantes.append(unidad)
            return True
        return False

    def atacante_gana_ronda(self):
        bases_vivas = [t for t in self.defensor.torres if t.fila == 0]
        if len(bases_vivas) < self.columnas:
            self.victorias_atacante += 1
            return True
            
        for u in self.rolatacante.atacantes:
            if u.fila < 0:  
                self.victorias_atacante += 1
                return True
        return False

    def defensor_gana_ronda(self):
        if self.tiempo_terminado():
            self.victorias_defensor += 1
            return True
        return False

    def ganador_final(self):
        if self.victorias_defensor == 3:
            return "Defensor"
        if self.victorias_atacante == 3:
            return "Atacante"
        return None

    def generar_ingreso_pasivo(self):
        tiempo_actual = time.time()
        if tiempo_actual - self.ultimo_ingreso_pasivo >= 1.0:
            self.defensor.dinero += 5
            self.rolatacante.dinero += 8
            self.ultimo_ingreso_pasivo = tiempo_actual

    def actualizar_ciclo_combate(self):
        if hasattr(self, 'pelea') and self.pelea:
            tiempo_actual = time.time()
            
            # MOVIMIENTO CALCULADO CORREGIDO SIN BUCLES INFINITOS
            for u in self.rolatacante.atacantes:
                intervalo_movimiento = 1.0 / u.velocidad
                if tiempo_actual - u.ultimo_movimiento >= intervalo_movimiento:
                    
                    # CORRECCIÓN DIRECTA: Verificamos de forma limpia si la casilla de arriba está ocupada
                    casilla_siguiente_ocupada = False
                    nueva_fila = u.fila - 1
                    
                    for t in self.defensor.torres:
                        if t.fila == nueva_fila and t.columna == u.columna:
                            casilla_siguiente_ocupada = True
                            break
                    
                    # Solo avanza si la casilla del frente está libre de estructuras defensoras
                    if not casilla_siguiente_ocupada:
                        u.fila = nueva_fila
                    
                    # Sincronizamos el tiempo de movimiento de la tropa
                    u.ultimo_movimiento = tiempo_actual
            
            # PROCESO DE ATAQUES Y LIMPIEZA DE OBJETOS MUERTOS
            self.pelea.ataque_torres()
            self.pelea.ataque_unidades()
            self.pelea.limpiar_objetos()