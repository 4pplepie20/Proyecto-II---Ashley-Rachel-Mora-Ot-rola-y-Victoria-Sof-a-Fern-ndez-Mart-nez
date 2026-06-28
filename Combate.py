class Combate:
    def __init__(self, defensor, rolatacante):
        self.defensor = defensor
        self.rolatacante = rolatacante
        self.dano_total_atacante = 0

    def mover_unidades(self):
        # El movimiento se gestiona de manera continua en el bucle de tiempo real
        pass

    def ataque_torres(self):
        for torres in self.defensor.torres:
            for unidad in self.rolatacante.atacantes:
                if torres.verificacion_rango(unidad):
                    torres.ataque(unidad)
                    torres.habilidad_especial(unidad)
                    break

    def ataque_unidades(self):
        for unidad in self.rolatacante.atacantes:
            ataco = False
            # 1. Ataque normal a las torres/defensas adyacentes
            for torres in self.defensor.torres:
                distancia = abs(unidad.fila - torres.fila) + abs(unidad.columna - torres.columna)
                if distancia <= 1:
                    unidad.ataque(torres)
                    unidad.habilidad_especial(torres)
                    self.dano_total_atacante += unidad.dano
                    ataco = True
                    break

            # 2. Si llegó al extremo superior (fila 0) y no ha atacado, daña la estructura base de esa columna
            if not ataco and unidad.fila <= 0:
                for torres in self.defensor.torres:
                    if torres.fila == 0 and torres.columna == unidad.columna:
                        unidad.ataque(torres)
                        unidad.habilidad_especial(torres)
                        self.dano_total_atacante += unidad.dano
                        break

    def limpiar_objects(self):
        # Mapeo idéntico por compatibilidad si es invocado por agentes externos
        self.limpiar_objetos()

    def limpiar_objetos(self):
        unidades_vivas = []
        for unidad in self.rolatacante.atacantes:
            # CORRECCIÓN: Cambiado 'u.vida' por 'unidad.vida' para evitar NameError
            if not unidad.destruida() and unidad.vida > 0:
                unidades_vivas.append(unidad)
            else:
                self.defensor.dinero += 20  # Recompensa directa al defensor
        self.rolatacante.atacantes = unidades_vivas

        torres_vivas = []
        for torres in self.defensor.torres:
            if not torres.destruida() and torres.vida > 0:
                torres_vivas.append(torres)
            else:
                self.rolatacante.dinero += 30  # Recompensa directa al atacante
        self.defensor.torres = torres_vivas