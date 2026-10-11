from datetime import timedelta
from configuracion import ConfiguracionSistema
from patrones import (
    PrioridadEstudiante, PrioridadCapitan, 
    CancelacionEstudiante, CancelacionCapitan, CancelacionAdmin
)

class Usuario:
    def __init__(self, nombre, mail):
        self.nombre = nombre
        self.mail = mail
        self.historial_noshows = [] 
        self.fecha_suspension_fin = None
        self.estrategia_prioridad = None
        self.estrategia_cancelacion = None

    def registrar_noshow(self, fecha_actual):
        config = ConfiguracionSistema()
        
        
        self.historial_noshows.append(fecha_actual)
        self.historial_noshows = [f for f in self.historial_noshows if f.month == fecha_actual.month and f.year == fecha_actual.year]
        
        total_mes = len(self.historial_noshows)
        print(f"  -> No-show registrado para {self.nombre}. Total este mes: {total_mes}")
        
        if total_mes >= config.limite_noshows:
            self.fecha_suspension_fin = fecha_actual + timedelta(days=config.dias_suspension)
            print(f"  -> ¡ALERTA! {self.nombre} suspendido por {config.dias_suspension} días.")
            self.historial_noshows.clear()

    def esta_suspendido(self, fecha_actual) -> bool:
        return self.fecha_suspension_fin and fecha_actual < self.fecha_suspension_fin

class Estudiante(Usuario):
    def __init__(self, nombre, mail, codigo_estudiante):
        super().__init__(nombre, mail)
        self.codigo_estudiante = codigo_estudiante
        self.estrategia_prioridad = PrioridadEstudiante()
        self.estrategia_cancelacion = CancelacionEstudiante()

class Capitan(Estudiante):
    def __init__(self, nombre, mail, codigo_estudiante, codigo_capitan):
        super().__init__(nombre, mail, codigo_estudiante)
        self.codigo_capitan = codigo_capitan
        self.estrategia_prioridad = PrioridadCapitan()
        self.estrategia_cancelacion = CancelacionCapitan()

class Cancha:
    def __init__(self, id_cancha):
        self.id_cancha = id_cancha

class Reserva:
    def __init__(self, id_reserva, fecha_inicio, fecha_final, cancha, usuario, estrategia_cancelacion):
        self.id = id_reserva
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.cancha = cancha
        self.usuario = usuario
        self.estrategia_cancelacion = estrategia_cancelacion
        self.estado = "Confirmada"

    def cancelar(self, fecha_actual, es_admin=False):
        estrategia = CancelacionAdmin() if es_admin else self.estrategia_cancelacion
        if estrategia.es_noshow(self.fecha_inicio, fecha_actual):
            self.estado = "No-Show"
            self.usuario.registrar_noshow(fecha_actual)
            print(f"Reserva {self.id} cancelada tarde. Registrada como NO-SHOW.")
        else:
            self.estado = "Cancelada"
            print(f"Reserva {self.id} cancelada a tiempo. Cancha liberada.")

class ReservaRegular(Reserva):
    pass

class ReservaOficial(Reserva):
    pass

#FACTORY METHOD
class CreadorReserva:
    _contador = 1
    @classmethod
    def crear_reserva(cls, fecha_inicio, fecha_final, cancha, usuario):
        id_res = f"R-{cls._contador}"
        cls._contador += 1
        if isinstance(usuario, Capitan):
            return ReservaOficial(id_res, fecha_inicio, fecha_final, cancha, usuario, usuario.estrategia_cancelacion)
        return ReservaRegular(id_res, fecha_inicio, fecha_final, cancha, usuario, usuario.estrategia_cancelacion)

#BUILDER
class ReservaRecurrenteBuilder:
    def __init__(self):
        self.reservas = []
        self.equipo = None
        self.notas = None

    def agregar_semana(self, reserva):
        self.reservas.append(reserva)
        return self

    def set_equipo(self, equipo):
        self.equipo = equipo
        return self

    def set_notas(self, notas):
        self.notas = notas
        return self

    def build(self):
        return {"reservas": self.reservas, "equipo": self.equipo, "notas": self.notas}