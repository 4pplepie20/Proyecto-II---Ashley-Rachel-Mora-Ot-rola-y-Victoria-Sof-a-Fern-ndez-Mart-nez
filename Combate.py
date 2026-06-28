class Combate:
    def __init__(self, defensor, rolatacante):
        self.defensor = defensor
        self.rolatacante = rolatacante
        self.dano_total_atacante = 0

    def mover_unidades(self):
        for unidad in self.rolatacante.atacantes:
            unidad.mover()

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
            for torres in self.defensor.torres:
                distancia = abs(unidad.fila - torres.fila) + abs(unidad.columna - torres.columna)

                if distancia <= 1:
                    unidad.ataque(torres)
                    unidad.habilidad_especial(torres)

                    self.dano_total_atacante += unidad.dano
                    ataco = True
                    break

            if not ataco:
                if unidad.fila >= 9:
                    unidad.ataque(self.defensor.base)
                    unidad.habilidad_especial(self.defensor.base)
                    self.dano_total_atacante += unidad.dano

    def limpiar_objetos(self):
        unidades_vivas = []
        for unidad in self.rolatacante.atacantes:
            if not unidad.destruida():
                unidades_vivas.append(unidad)
            else:
                self.defensor.ganar_dinero(20)
        self.rolatacante.atacantes = unidades_vivas

        torres_vivas = []


        for torres in self.defensor.torres:
            if not torres.destruida():
                torres_vivas.append(torres)
            else:
                self.rolatacante.ganar_dinero(30)
        self.defensor.torres = torres_vivas

    def actualizar_combate(self):
        self.mover_unidades()
        self.ataque_torres()
        self.ataque_unidades()
        self.limpiar_objetos()