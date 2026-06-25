
class LogicaPuntajes:
    def __init__(self, gestor_usuarios): # Recibe el gestor de usuarios para leer la lista de jugadores 
        self.gestor = gestor_usuarios

    def obtener_ranking_general(self): 
        lista_jugadores = self.gestor.lista_usuarios #Devuelve la lista ordenada por victorias totales (Atacante+ Defensor)
        
        def calcular_total(usuario): # Calcula el putaje total
            return usuario.obtener_victorias_atacante() + usuario.obtener_victorias_defensor()
        return sorted(lista_jugadores, key=calcular_total, reverse=True) #Devuelve los resultados en una lista de mayor a menor

    def obtener_ranking_atacante(self):
        lista_jugadores = self.gestor.lista_usuarios # Devuelve la lista ordenada ÚNICAMENTE por victorias de Atacante
        
        def calcular_atacante(usuario): #Calcula unicamente las victorias en atacante
            return usuario.obtener_victorias_atacante()      
        return sorted(lista_jugadores, key=calcular_atacante, reverse=True) #Devuelve una lista de mayor a menor de los puntajes en atacante

    def obtener_ranking_defensor(self):
        lista_jugadores = self.gestor.lista_usuarios # Devuelve la lista ordenada ÚNICAMENTE por victorias de Defensor
        
        def calcular_defensor(usuario): #Calcula unicamente las victorias en defensor
            return usuario.obtener_victorias_defensor()
        return sorted(lista_jugadores, key=calcular_defensor, reverse=True) # Devuelve la lista  ordenada de mayor a menor de los puntajes en defensor