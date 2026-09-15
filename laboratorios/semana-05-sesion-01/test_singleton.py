from singleton import GestorDeConfiguracion, reserva_permitida

def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto()
    config.modo_mantenimiento = True

    assert reserva_permitida(config) is False
def test_reserva_aceptada():
    config = GestorDeConfiguracion.obtener_objeto()
    #solucion---------------------------
    config.modo_mantenimiento = False
    #-----------------------------------
    assert reserva_permitida(config) is True

#la variable es global entonces falla ya que en la primera prueba se asigna como true,
#,cambiando la instancia de ese unico objeto
