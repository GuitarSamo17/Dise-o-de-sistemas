from datetime import datetime, timedelta
import threading
from entidades import Estudiante, Capitan, Cancha
from patrones import BloqueoMantenimiento
from fachada import ReservaUFacade

def main():
    facade = ReservaUFacade()
    hoy = datetime(2026, 10, 15, 10, 0)
    
    estudiante = Estudiante("Juan", "juan@mail.com", "EST123")
    capitan = Capitan("Ana", "ana@mail.com", "EST456", "CAP001")
    
    for c_id in ["C-01", "C-02", "C-03", "C-04"]:
        facade.agregar_cancha(Cancha(c_id))

    print("\n--- ESCENARIO 1: Reserva en cada sede (Validada y notificada) ---")
    facade.reservar("Norte", "C-01", hoy.replace(hour=14), estudiante, hoy)
    print("-" * 30)
    facade.reservar("Sur", "C-02", hoy.replace(hour=15), capitan, hoy)

    print("\n--- ESCENARIO 2: Reserva rechazada por horario de la sede ---")
    _, msg = facade.reservar("Norte", "C-03", hoy.replace(hour=5), estudiante, hoy)
    print(f"Resultado: {msg}")

    print("\n--- ESCENARIO 3: Recurrente exitosa y rechazada por conflicto ---")
    facade.reservar_recurrente("Sur", "C-03", hoy.replace(hour=18), 3, capitan, hoy)
    print("\nIntentando reservar más de 8 semanas...")
    _, msg_limite = facade.reservar_recurrente("Sur", "C-04", hoy.replace(hour=18), 10, capitan, hoy)
    print(f"Resultado: {msg_limite}")
    
    print("\nIntentando causar conflicto en la semana 2...")
    _, msg_conflicto = facade.reservar_recurrente("Sur", "C-03", hoy.replace(hour=18) + timedelta(weeks=1), 2, capitan, hoy)
    print(f"Resultado: {msg_conflicto}")

    print("\n--- ESCENARIO 4: Tres cancelaciones con resultados distintos ---")
    r1, _ = facade.reservar("Norte", "C-01", hoy + timedelta(hours=3), estudiante, hoy)
    facade.cancelar(r1.id, hoy)

    r2, _ = facade.reservar("Norte", "C-01", hoy + timedelta(hours=12), capitan, hoy)
    facade.cancelar(r2.id, hoy)

    r3, _ = facade.reservar("Norte", "C-01", hoy + timedelta(hours=1), estudiante, hoy)
    facade.cancelar(r3.id, hoy, es_admin=True)

    print("\n--- ESCENARIO 5: Suspensión por 3 No-shows en el mes ---")
    print("Generando 2 No-shows adicionales para Ana...")
    for i in range(2):
        r, _ = facade.reservar("Sur", "C-04", hoy + timedelta(hours=1), capitan, hoy)
        facade.cancelar(r.id, hoy)
        
    print("\nIntento de reserva estando suspendida:")
    _, msg = facade.reservar("Sur", "C-01", hoy + timedelta(days=1), capitan, hoy)
    print(f"Resultado: {msg}")

    print("\n--- ESCENARIO 6: Bloqueo clonado de Admin ---")
    plantilla = BloqueoMantenimiento("Torneo Semestral", ["Red nueva"])
    r4, _ = facade.reservar("Norte", "C-02", hoy + timedelta(days=2), estudiante, hoy)
    facade.bloquear(plantilla, ["C-02", "C-03"], hoy + timedelta(days=2), hoy, "Norte")

    print("\n--- ESCENARIO 7: Concurrencia (Dos hilos al mismo tiempo) ---")
    resultados = []
    def intento_reserva(hilo_nombre):
        print(f"Hilo {hilo_nombre} intentando reservar...")
        _, msg = facade.reservar("Norte", "C-04", hoy + timedelta(days=3), estudiante, hoy)
        resultados.append(f"Hilo {hilo_nombre} obtuvo: {msg}")
        
    t1 = threading.Thread(target=intento_reserva, args=("A",))
    t2 = threading.Thread(target=intento_reserva, args=("B",))
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    for res in resultados:
        print(res)

if __name__ == "__main__":
    main()