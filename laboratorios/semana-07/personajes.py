from abc import ABC

class Personaje(ABC):
    def __init__(self, nombre: str, vida: int, ataque: int):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    def recibir_dano(self, dano: int):
        self.vida -= dano
        if self.vida < 0:
            self.vida = 0

class Guerrero(Personaje):
    def __init__(self): super().__init__("Guerrero", 100, 15)

class Dragon(Personaje):
    def __init__(self): super().__init__("Dragón", 150, 20)

class Soldado(Personaje):
    def __init__(self): super().__init__("Soldado", 90, 18)

class Alien(Personaje):
    def __init__(self): super().__init__("Alien", 120, 22)
