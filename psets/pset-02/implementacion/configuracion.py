class ConfiguracionSistema:
    "Singleton"
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConfiguracionSistema, cls).__new__(cls)
           
            cls._instancia.ventana_estudiante = 2
            cls._instancia.ventana_capitan = 24
            cls._instancia.limite_noshows = 3
            cls._instancia.dias_suspension = 7
            cls._instancia.hora_limite_prioridad = 18 
        return cls._instancia
