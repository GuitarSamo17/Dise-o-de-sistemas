
from personajes import Personaje, Guerrero, Dragon, Soldado, Alien
from abc import ABC, abstractmethod

class MundoFactory(ABC):
    @abstractmethod
    def crear_jugador(self) -> Personaje: pass
    
    @abstractmethod
    def crear_enemigo(self) -> Personaje: pass

class FantasyFactory(MundoFactory):
    def crear_jugador(self) -> Personaje:
        return PersonajeFactory.crear("guerrero")
    
    def crear_enemigo(self) -> Personaje:
        return PersonajeFactory.crear("dragon")

class SciFiFactory(MundoFactory):
    def crear_jugador(self) -> Personaje:
        return PersonajeFactory.crear("soldado")
    
    def crear_enemigo(self) -> Personaje:
        return PersonajeFactory.crear("alien")


class PersonajeFactory:
    @staticmethod
    def crear(tipo: str) -> Personaje:
        tipo = tipo.lower()
        if tipo == "guerrero": return Guerrero()
        elif tipo == "dragon": return Dragon()
        elif tipo == "soldado": return Soldado()
        elif tipo == "alien": return Alien()
        else: raise ValueError(f"Tipo de personaje desconocido: {tipo}")