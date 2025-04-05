# restaurante.py

from mesa import Mesa

class Restaurante:
    def __init__(self):
        self.mesas = [
            Mesa(1, 150, 200), Mesa(2, 300, 200),
            Mesa(3, 450, 200), Mesa(4, 600, 200),
            Mesa(5, 150, 400), Mesa(6, 300, 400),
            Mesa(7, 450, 400), Mesa(8, 600, 400)
        ]

    def get_posicion_mesa(self, numero):
        for mesa in self.mesas:
            if mesa.numero == numero:
                return mesa.posicion
        return None
