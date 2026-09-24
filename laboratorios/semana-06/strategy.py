from abc import ABC, abstractmethod

class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar(self, precio_base):
        pass

class SinDescuento(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base
class DescuentoVIP(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base*0.80
class DescuentoEstudiante(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base*0.95
class DescuentoEmpleado(EstrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base*0.75

class Compra:
    def __init__(self, EstrategiaDescuento):
        self.EstrategiaDescuento = EstrategiaDescuento
    def calcular_total(self,precio):
        return self.EstrategiaDescuento.aplicar(precio)





def main():
    sin_descuento = SinDescuento()
    descuento_vip = DescuentoVIP()
    descuento_estudiante = DescuentoEstudiante()
    descuento_empleado = DescuentoEmpleado()

    compra_1 = Compra(sin_descuento)
    print(compra_1.calcular_total(100))

    compra_2 = Compra(descuento_vip)
    print(compra_2.calcular_total(100))

    compra_3 = Compra(descuento_estudiante)
    print(compra_3.calcular_total(100))

    compra_4 = Compra(descuento_empleado)
    print(compra_4.calcular_total(100))

if __name__ == "__main__":
  main()

    #if tipo_usuario== "normal":
        #precio_normal()
    #elif tipo_usuario=="VIP":
     #   precio_descuento()
    #elif tipo_usuario=="estudiante":
     #   precio_estudiante()
