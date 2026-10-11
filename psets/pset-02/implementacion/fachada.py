import threading
from datetime import timedelta
from patrones import SedeNorteFactory, SedeSurFactory
from entidades import CreadorReserva, ReservaRecurrenteBuilder

class ReservaUFacade:
    def __init__(self):
        self.lock = threading.Lock()
        self.sedes = {"Norte": SedeNorteFactory(), "Sur": SedeSurFactory()}
        self.canchas_bd = []
        self.reservas_bd = []

    def agregar_cancha(self, cancha):
        self.canchas_bd.append(cancha)

    def _esta_disponible(self, cancha_id, fecha_inicio):
        for r in self.reservas_bd:
            if r.cancha.id_cancha == cancha_id and r.fecha_inicio == fecha_inicio and r.estado == "Confirmada":
                return False
        return True

    def reservar(self, sede_nombre, cancha_id, fecha_inicio, usuario, fecha_actual):
        print(f"  [Paso 1] Verificando suspensión de {usuario.nombre}...")
        if usuario.esta_suspendido(fecha_actual):
            return None, f"Rechazo: {usuario.nombre} suspendido."

        print(f"  [Paso 2] Validando horario en Sede {sede_nombre}...")
        fabrica = self.sedes[sede_nombre]
        if not fabrica.crear_validador().es_valido(fecha_inicio.hour):
            return None, f"Rechazo: {fecha_inicio.hour}:00 fuera de horario en {sede_nombre}."

        print(f"  [Paso 3] Adquiriendo candado (Lock) y verificando disponibilidad de {cancha_id}...")
        with self.lock:
            if not self._esta_disponible(cancha_id, fecha_inicio):
                return None, f"Rechazo: Cancha {cancha_id} ocupada."

            print("  [Paso 4] Creando reserva...")
            cancha = next((c for c in self.canchas_bd if c.id_cancha == cancha_id), None)
            nueva_reserva = CreadorReserva.crear_reserva(fecha_inicio, fecha_inicio + timedelta(hours=1), cancha, usuario)
            
            tipo = "CON PRIORIDAD" if usuario.estrategia_prioridad.tiene_prioridad(fecha_inicio.hour) else "SIN PRIORIDAD"
            self.reservas_bd.append(nueva_reserva)
            
        
        print("  [Paso 5] Notificando confirmación...")
        fabrica.crear_notificador().notificar(f"Reserva {nueva_reserva.id} confirmada para {usuario.nombre} ({tipo}).")
        return nueva_reserva, "Éxito"

    def reservar_recurrente(self, sede_nombre, cancha_id, fecha_inicio, semanas, usuario, fecha_actual):
        print(f"  [Recurrente] Solicitud de {semanas} semanas para {usuario.nombre} en {cancha_id}")
        if not (2 <= semanas <= 8):
            return None, f"Rechazo: La reserva recurrente debe ser entre 2 y 8 semanas (Solicitadas: {semanas})."
        
        fechas = [fecha_inicio + timedelta(weeks=i) for i in range(semanas)]
        
        print("  [Recurrente] Verificando disponibilidad (Regla todo o nada)...")
        with self.lock:
            for i, f in enumerate(fechas):
                if not self._esta_disponible(cancha_id, f):
                    return None, f"Rechazo: Conflicto en semana {i+1} ({f}). No se registró nada."

            print("  [Recurrente] Construyendo paquete de reservas...")
            cancha = next((c for c in self.canchas_bd if c.id_cancha == cancha_id), None)
            builder = ReservaRecurrenteBuilder()
            
            for f in fechas:
                res = CreadorReserva.crear_reserva(f, f + timedelta(hours=1), cancha, usuario)
                self.reservas_bd.append(res)
                builder.agregar_semana(res)
            
            paquete = builder.set_equipo(["Chalecos", "Balones"]).build()
            
        self.sedes[sede_nombre].crear_notificador().notificar(f"Recurrente confirmada por {semanas} semanas para {usuario.nombre}.")
        return paquete, "Éxito"

    def cancelar(self, id_reserva, fecha_actual, es_admin=False):
        with self.lock:
            reserva = next((r for r in self.reservas_bd if r.id == id_reserva), None)
            if reserva and reserva.estado == "Confirmada":
                reserva.cancelar(fecha_actual, es_admin)
                return True
            return False

    def bloquear(self, plantilla, canchas_ids, fecha, fecha_actual, sede_nombre):
        with self.lock:
            notificador = self.sedes[sede_nombre].crear_notificador()
            for c_id in canchas_ids:
                clon = plantilla.clonar()
                for r in self.reservas_bd:
                    if r.cancha.id_cancha == c_id and r.fecha_inicio == fecha and r.estado == "Confirmada":
                        r.cancelar(fecha_actual, es_admin=True)
                        notificador.notificar(f"Atención {r.usuario.nombre}: Reserva {r.id} anulada por {clon.motivo}.")
                print(f"  [Admin] Bloqueo clonado y aplicado en {c_id}.")