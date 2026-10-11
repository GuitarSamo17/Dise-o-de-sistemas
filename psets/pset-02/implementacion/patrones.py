import copy
from abc import ABC, abstractmethod
from datetime import timedelta
from configuracion import ConfiguracionSistema

#STRATEGY: Prioridad y Cancelación
class EstrategiaPrioridad(ABC):
    @abstractmethod
    def tiene_prioridad(self, hora) -> bool: pass

class PrioridadEstudiante(EstrategiaPrioridad):
    def tiene_prioridad(self, hora) -> bool: return False

class PrioridadCapitan(EstrategiaPrioridad):
    def tiene_prioridad(self, hora) -> bool:
        config = ConfiguracionSistema()
        return hora < config.hora_limite_prioridad 

class EstrategiaCancelacion(ABC):
    @abstractmethod
    def es_noshow(self, fecha_inicio, fecha_cancelacion) -> bool: pass

class CancelacionEstudiante(EstrategiaCancelacion):
    def es_noshow(self, fecha_inicio, fecha_cancelacion) -> bool:
        config = ConfiguracionSistema()
        limite = fecha_inicio - timedelta(hours=config.ventana_estudiante)
        return fecha_cancelacion > limite

class CancelacionCapitan(EstrategiaCancelacion):
    def es_noshow(self, fecha_inicio, fecha_cancelacion) -> bool:
        config = ConfiguracionSistema()
        limite = fecha_inicio - timedelta(hours=config.ventana_capitan)
        return fecha_cancelacion > limite

class CancelacionAdmin(EstrategiaCancelacion):
    def es_noshow(self, fecha_inicio, fecha_cancelacion) -> bool:
        return False 

#ABSTRACT FACTORY:Sedes 
class ValidadorHorario(ABC):
    @abstractmethod
    def es_valido(self, hora) -> bool: pass

class Notificador(ABC):
    @abstractmethod
    def notificar(self, mensaje): pass

class FabricaSede(ABC):
    @abstractmethod
    def crear_validador(self) -> ValidadorHorario: pass
    @abstractmethod
    def crear_notificador(self) -> Notificador: pass

class SedeNorteFactory(FabricaSede):
    class ValidadorNorte(ValidadorHorario):
        def es_valido(self, hora) -> bool: return 6 <= hora <= 22
    class NotificadorNorte(Notificador):
        def notificar(self, mensaje): print(f"[Correo Sede Norte] {mensaje}")
    def crear_validador(self): return self.ValidadorNorte()
    def crear_notificador(self): return self.NotificadorNorte()

class SedeSurFactory(FabricaSede):
    class ValidadorSur(ValidadorHorario):
        def es_valido(self, hora) -> bool: return 7 <= hora <= 23
    class NotificadorSur(Notificador):
        def notificar(self, mensaje): print(f"[SMS Sede Sur] {mensaje}")
    def crear_validador(self): return self.ValidadorSur()
    def crear_notificador(self): return self.NotificadorSur()

#PROTOTYPE: Bloqueo de Administrador
class BloqueoMantenimiento:
    def __init__(self, motivo, equipo_necesario=None):
        self.motivo = motivo
        self.equipo_necesario = equipo_necesario or []
        self.cancha = None
        self.fecha = None

    def clonar(self):
        return copy.deepcopy(self)