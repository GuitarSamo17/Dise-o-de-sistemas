from datetime import datetime, timedelta

class Usuario:
    def __init__(self, nombre, mail):
        self.nombre = nombre
        self.mail = mail

class Estudiante(Usuario):
    def __init__(self, nombre, mail, codigo_estudiante):
        super().__init__(nombre, mail)
        self.codigo_estudiante = codigo_estudiante

    def PrioridadEstudiante(self, hora):
        return False

class Capitan(Estudiante):
    def __init__(self, nombre, mail, codigo_estudiante, codigo_capitan):
        super().__init__(nombre, mail, codigo_estudiante)
        self.codigo_capitan = codigo_capitan

    def PrioridadCapitan(self, hora):
        return hora < 18

class Cancha:
    def __init__(self, id_cancha):
        self.id_cancha = id_cancha
        self._esta_disponible = True  

    def disponibilidad(self):
        return self._esta_disponible

    @staticmethod
    def ver_canchas_disponibles(lista_canchas):
        print("\n--- CONSULTANDO CANCHAS DISPONIBLES ---")
        canchas_libres = [c for c in lista_canchas if c.disponibilidad()]
        if not canchas_libres:
            print("-> No hay canchas disponibles en este momento.")
        for c in canchas_libres:
            print(f"-> Cancha disponible ID: {c.id_cancha}")
        return canchas_libres

class ReglaPrioridad:
    def __init__(self, hora_actual):
        self.Hora_Actual = hora_actual

    def esPrioritaria(self, usuario, hora):
        metodo_prioridad = getattr(usuario, "PrioridadCapitan", getattr(usuario, "PrioridadEstudiante"))
        return metodo_prioridad(hora)

class Reserva:
    def __init__(self, id_reserva, hora, estado, fecha_inicio, fecha_final, cancha, regla_prioridad):
        self.id = id_reserva
        self.hora = hora
        self.estado = estado
        self.fecha_inicio = fecha_inicio
        self.fecha_final = fecha_final
        self.cancha = cancha
        self.regla_prioridad = regla_prioridad

    def añadir(self, usuario):
        if self.cancha.disponibilidad():
            prioridad = self.regla_prioridad.esPrioritaria(usuario, self.hora)
            self.estado = "Confirmada"
            self.cancha._esta_disponible = False
            tipo = "CON PRIORIDAD" if prioridad else "SIN PRIORIDAD"
            print(f"Reserva {self.id} realizada por {usuario.nombre} en cancha {self.cancha.id_cancha} ({tipo}).")
        else:
            self.estado = "Rechazada"
            print(f"Error al añadir: La cancha {self.cancha.id_cancha} ya no está disponible.")

    def cancelar(self):
        # Se integra la regla de negocio del no-show
        if self.esNoshow(self.fecha_inicio):
            self.estado = "No-Show"
            print(f"Reserva {self.id} cancelada con menos de 2 horas. Registrada como NO-SHOW. (La cancha no se libera)")
        else:
            self.estado = "Cancelada"
            self.cancha._esta_disponible = True
            print(f"Reserva {self.id} cancelada de forma regular. Cancha liberada.")

    def esNoshow(self, fecha_inicio):
        ahora = datetime.now()
        tiempo_restante = fecha_inicio - ahora
        return tiempo_restante < timedelta(hours=2)

class Administrador:
    def __init__(self, nombre, codigo_administrador):
        self.nombre = nombre
        self.codigo_administrador = codigo_administrador

    def gestion_disponibilidad(self, id_cancha, cancha_obj, nuevo_estado):
        cancha_obj._esta_disponible = nuevo_estado
        estado_str = "Disponible" if nuevo_estado else "Ocupada"
        print(f"Admin {self.nombre}: La cancha {id_cancha} ahora está {estado_str}.")

    def conflictos_reserva(self, id_reserva, reserva_obj):
        reserva_obj.estado = "Intervenida por Admin"
        print(f"Admin {self.nombre}: Conflicto resuelto en la reserva {id_reserva}.")

if __name__ == "__main__":
    lista_canchas = [Cancha("C-01"), Cancha("C-02"), Cancha("C-03")]
    
    reglas = ReglaPrioridad(hora_actual="14:00")
    admin = Administrador("Carlos", "ADM-999")
    
    estudiante = Estudiante("Juan", "juan@mail.com", "EST123")
    capitan = Capitan("Ana", "ana@mail.com", "EST456", "CAP001")
    
    hora_solicitud = 15 
    inicio_partido = datetime.now() + timedelta(hours=5)
    fin_partido = inicio_partido + timedelta(hours=1)

    print("\n[Prueba 1: Capitán visualiza canchas y realiza reserva]")
    canchas_libres_1 = Cancha.ver_canchas_disponibles(lista_canchas)
    reserva_capitan = Reserva("R-1", hora_solicitud, "Pendiente", inicio_partido, fin_partido, canchas_libres_1[0], reglas)
    reserva_capitan.añadir(capitan)

    print("\n[Prueba 2: Estudiante visualiza canchas y realiza reserva]")
    canchas_libres_2 = Cancha.ver_canchas_disponibles(lista_canchas)
    reserva_estudiante = Reserva("R-2", hora_solicitud, "Pendiente", inicio_partido, fin_partido, canchas_libres_2[0], reglas)
    reserva_estudiante.añadir(estudiante)

    print("\n[Prueba 3: Cancelación Regular de Estudiante]")
    reserva_estudiante.cancelar()

    print("\n[Prueba 4: Intervención del Administrador]")
    admin.gestion_disponibilidad("C-02", lista_canchas[1], False)
    admin.conflictos_reserva("R-1", reserva_capitan)
    print(f"Estado final de la reserva R-1: {reserva_capitan.estado}")

    print("\n[Prueba 5: Cancelación tardía (Genera No-Show)]")
   
    inicio_inminente = datetime.now() + timedelta(hours=1)
    reserva_tardia = Reserva("R-3", hora_solicitud, "Pendiente", inicio_inminente, inicio_inminente + timedelta(hours=1), lista_canchas[2], reglas)
    reserva_tardia.añadir(estudiante)
    
    reserva_tardia.cancelar()

    print("\n[Prueba 6: Intento de reserva en cancha ocupada]")
    reserva_fallida = Reserva("R-4", hora_solicitud, "Pendiente", inicio_partido, fin_partido, lista_canchas[0], reglas)
    reserva_fallida.añadir(estudiante)