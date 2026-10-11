# ReservaU - PSet 2

## Tabla de Patrones y Justificación

| Patrón | Requerimiento que lo justifica | Problema que resuelve | Clases y métodos |
| :--- | :--- | :--- | :--- |
| Strategy | RF-09: Reglas de cancelación según el rol. | Extrae la lógica de prioridad y cancelación de la entidad Reserva. Evita un if gigante para decidir cómo cancelar. | EstrategiaCancelacion, EstrategiaPrioridad |
| Singleton | RF-15: Centralización de reglas. | Garantiza que la configuración de reglas viva en un único lugar del sistema. Evita buscar números mágicos esparcidos por el código. | ConfiguracionSistema, __new__() |
| Factory Method | RF-02 y RF-09: Registrar reserva y asignar políticas por rol. | La decisión de qué clase instanciar reside en un solo lugar. Asigna automáticamente la política de cancelación (Estudiante vs Capitán). | CreadorReserva, crear_reserva() |
| Abstract Factory | RF-13 y RF-14: Reglas y avisos por sede (Norte y Sur). | Impide combinar accidentalmente el validador de horario de una sede con el notificador de la otra. | FabricaSede (Norte/Sur), crear_validador(), crear_notificador() |
| Builder | RF-07: Reservas recurrentes con datos opcionales. | Permite construir un objeto complejo paso a paso, manejando datos obligatorios y opcionales (equipo, notas) de forma limpia. | ReservaRecurrenteBuilder, set_equipo(), build() |
| Prototype | RF-11: Bloqueo tipo plantilla por el Administrador. | Permite definir un bloqueo una sola vez y clonarlo para distintas fechas/canchas sin afectar la plantilla original. | BloqueoMantenimiento, clonar() |
| Facade | RF-07, RF-11 y RNF-01: Coordinación y concurrencia. | Oculta la complejidad de interactuar con disponibilidad, sedes, notificaciones y no-shows. simulacion.py solo habla con la Facade. | ReservaUFacade, reservar(), cancelar() |

### Decisiones de Diseño Adicionales

* Uso de copy.deepcopy en Prototype: Utilizamos deepcopy porque el bloqueo podría contener listas anidadas (por ejemplo, listas de equipos a montar). Un copy superficial (shallow copy) compartiría la referencia de la lista de equipos entre los clones, haciendo que si modificamos el equipo de un clon, se altere la plantilla original.
* Concurrencia (Locking Pesimista vs Optimista): Se implementó un Locking Pesimista (threading.Lock en la Facade). Se justifica por el requerimiento RNF-01, ya que existen picos de escritura al inicio de cada semestre donde las colisiones (dos intentando reservar la misma cancha/franja) son altamente probables. El locking pesimista protege la sección crítica asumiendo que el conflicto ocurrirá, evitando el incidente de la doble reserva.
* Singleton (Pros y Contras): Ganamos un punto de acceso global y consistente para las reglas de negocio, cumpliendo el RF-15 sin instanciar el objeto repetidamente. El costo aceptado es que introducimos un estado global, lo que puede complicar un poco las pruebas unitarias si los valores necesitan ser reiniciados entre tests.