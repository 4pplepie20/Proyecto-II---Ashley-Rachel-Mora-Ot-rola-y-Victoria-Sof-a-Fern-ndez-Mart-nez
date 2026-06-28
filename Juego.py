import time
from Combate import Combate
from Torres import TorreBasica, TorrePesada, TorreMagica, TorrePrincipal, Torres
from Atacante import SoldadoBasico, Tanque, Explorador

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
        self.dano_anterior_atacante = 0
    
    def iniciar_ronda(self):
        self.inicio_ronda = time.time()
        self.defensor.dinero += 100
        self.rolatacante.dinero += 100

        bono_atacante = self.dano_anterior_atacante // 5
        
        self.rolatacante.dinero += bono_atacante

    def tiempo_terminado(self):
        tiempo_actual = time.time()
        tiempo_trascurrido = tiempo_actual - self.inicio_ronda
        if tiempo_trascurrido >= self.tiempo_ronda:
            return True
        return False
    
    def posicion_valida_defensor(self, fila):
        if 0 <= fila <= 3:
            return True
        return False
    
    def posicion_valida_atacante(self, fila):
        if 6 <= fila <= 9:
            return True
        return False
    
    def casilla_ocupada(self, fila, columna):
        for torres in self.defensor.torres:
            if torres.fila == fila and torres.columna == columna:
                return True
        
        for unidad in self.rolatacante.atacantes:
            if unidad.fila == fila and columna == columna:
                return True
        
        return False
    
    def comprar_torre(self, torres, fila, columna):
        if columna < 0 or columna >= self.columnas:
            return False
        
        if not self.posicion_valida_defensor(fila):
            return False
        
        if self.casilla_ocupada(fila, columna):
            return False
        
        if self.defensor.comprar_torres(torres):
            torres.fila = fila
            torres.columna = columna
            return True 
        return False
        
    def comprar_unidad(self, unidad, fila, columna):
        if columna < 0 or columna >= self.columnas:
            return False
        
        if not self.posicion_valida_atacante(fila):
            return False
        
        if self.casilla_ocupada(fila, columna):
            return False
        
        if self.rolatacante.comprar_unidad(unidad):
            unidad.fila = fila
            unidad.columna = columna
            return True
        return False

    def atacante_gana_ronda(self):
        if self.defensor.base.destruida():
            self.victorias_atacante += 1
            return True
        return False

    def defensor_gana_ronda(self):
        if len(self.rolatacante.atacantes) == 0:
            unidad_mas_barata = 999999

            for unidad in self.rolatacante.catalogo_unidades:
                if unidad.costo < unidad_mas_barata:
                    unidad_mas_barata = unidad.costo

            if self.rolatacante.dinero < unidad_mas_barata:
                self.victorias_defensor += 1
                return True
            
        return False

    def empate_ronda(self):
        if self.tiempo_terminado():
            return True
        return False

    def ganador_final(self):

        if self.victorias_defensor == 3:
            return True

        if self.victorias_atacante == 3:
            return True
        
        return False

    def ejecutar_ronda(self):
        self.iniciar_ronda()
        pelea = Combate(self.defensor, self.rolatacante)

        while True:
            pelea.actualizar_combate()
            time.sleep(1)

            if self.atacante_gana_ronda():
                break

            if self.defensor_gana_ronda():
                break

            if self.empate_ronda():
                break
        
        self.dano_anterior_atacante = pelea.dano_total_atacante

    def ejecutar_juego(self):
        while True:
            self.ejecutar_ronda()

            if self.ganador_final():
                break
            self.ronda += 1