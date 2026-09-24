class Inventario:
    def verificar(self, producto)
        print(f'Verificando el stock de {producto}')
        return True
class Pago:
    def procesar(self, monto):
        print(f'Procesando pago: {monto}')
        return True
class Envio:
    def crear_envio(self, producto):
        print(f'Preparando el envio del {producto}')

#fachada
class TiendaFacade:
    def __init__(self):
        self.inventario = Inventario()
        self.pago = Pago()
        self.envio = Envio()
    def comprar(self, producto, precio):
        if not self.inventario.verificar(producto):
            print('No hay stock')
            return
        if not self.pago.procesar(precio):
            print('Fallo el pago')
            return

        self.envio.crear_envio(producto)
        print('Compra completada')

def main():

    tienda = TiendaFacade()
    tienda.comprar('Laptop',1500)

if __name__ == "__main__":
  main()

    #inventario= Inventario()
    #motor_pago = Pago()
    #motor_envio = Envio()

    #if inventario.verificar('Laptop'):
     #   pago = motor_pago.procesar(1500)

      #  if pago:
       #     motor_envio.crear_envio('Laptop')
        #else:
         #   print('Fallo el pago')
    #else:
     #   print('No hay inventario')
