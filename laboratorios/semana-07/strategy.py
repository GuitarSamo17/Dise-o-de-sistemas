from abc import ABC, abstractmethod

class EstrategiaAtaque(ABC):
    @abstractmethod
    def calcular_dano(self, ataque_base: int) -> int:
        pass

class AtaqueNormal(EstrategiaAtaque):
    def calcular_dano(self, ataque_base: int) -> int:
        return ataque_base  

class AtaqueFuerte(EstrategiaAtaque):
    def calcular_dano(self, ataque_base: int) -> int:
        return int(ataque_base * 1.5)  