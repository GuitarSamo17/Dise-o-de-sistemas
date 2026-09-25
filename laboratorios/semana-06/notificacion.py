class Mensaje:
    def enviar(self, mensaje):
        print(f'{mensaje}')
        return True
class Envio:
    def crear_envio(self,estado):
        print(f'Preparando el envio del mensaje {estado}')
        return True

class MailFacade:
    def __init__(self):
        self.mensaje1 = Mensaje()
        self.envio = Envio()
    def mandar_mensaje(self, mensaje, estado):
        if not self.envio.crear_envio(estado):
            print(f'No se pudo enviar el mensaje {estado}')
            return
        self.mensaje1.enviar(mensaje)
        print('Mensaje enviado')

def main():

    mail = MailFacade()
    mail.mandar_mensaje('Hola',"estable")

if __name__ == "__main__":
  main()
