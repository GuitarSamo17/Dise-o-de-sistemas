class Vehiculo:
    def __init__(self, caracteristica_movimiento):
        self.caracteristica_movimiento= caracteristica_movimiento
    def mover(self):
        self.caracteristica_movimiento.mover()

class CaracteristicaMovimiento:
    def mover(self):
        raise NotImplementedError
class MovimientoCarretera(CaracteristicaMovimiento):
    def mover(self):
        print("Conduciendo por carretera")
class MovimientoMar(CaracteristicaMovimiento):
    def mover(self):
        print("Navegando por agua")  
class MovimientoCielo(CaracteristicaMovimiento):
    def mover(self):
        print("Volando por el aire")

class Auto(Vehiculo):
    def __init__(self):
        carretera = MovimientoCarretera()
        super().__init__(carretera)
class Bote(Vehiculo):
    def __init__(self):
        mar = MovimientoMar()
        super().__init__(mar)
class Avion(Vehiculo):
    def __init__(self):
        cielo = MovimientoCielo()
        super().__init__(cielo)

if __name__ == "__main__":
    auto = Auto()
    auto.mover()
    bote = Bote()
    bote.mover()
    avion= Avion()
    avion.mover()
