import json

class Usuario:
    def __init__(self, usuario, contrasena, victorias_atacante = 0, victorias_defensor = 0):
        self.usuario = usuario
        self.contrasena = contrasena
        self.victorias_atacante = victorias_atacante
        self.victorias_defensor = victorias_defensor

    def obtener_nombre(self):
        return self.usuario
    
    def obtener_contrasena(self):
        return self.obtener_contrasena
    
    def obtener_victorias_atacante(self):
        return self.victorias_atacante 
    
    def obtener_victorias_defensor(self):
        return self.victorias_defensor
    
    def nueva_victoria_atacante(self):
        self.victorias_atacante += 1
    
    def nueva_victoria_defensor(self):
        self.victorias_defensor += 1
    
    


        
class Regitro: