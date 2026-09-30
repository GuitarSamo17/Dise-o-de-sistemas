from config import GameConfig
from factory import FantasyFactory, SciFiFactory
from strategy import AtaqueNormal, AtaqueFuerte

class GameFacade:
    def __init__(self, tipo_mundo: str):
        
        self.config = GameConfig.obtener_objeto()
        
        
        if tipo_mundo == "fantasia":
            factory = FantasyFactory()
        elif tipo_mundo == "scifi":
            factory = SciFiFactory()

            
        
        self.jugador = factory.crear_jugador()
        self.enemigo = factory.crear_enemigo()
        
        
        self.estrategia_actual = AtaqueNormal()

    def jugar(self):
        print(f"\n--- INICIO DEL COMBATE: {self.jugador.nombre} vs {self.enemigo.nombre} ---")
        print(f"Max Turnos: {self.config.numero_maximo_turnos} | Dificultad: {self.config.dificultad}\n")
        
        turno_actual = 1
        
        while self.jugador.vida > 0 and self.enemigo.vida > 0 and turno_actual <= self.config.numero_maximo_turnos:
            print(f"--- Turno {turno_actual} ---")
            print(f"Tu vida: {self.jugador.vida} | Vida enemigo: {self.enemigo.vida}")
            
            
            opcion = input("Elige tu ataque (1: Normal, 2: Fuerte): ")
            if opcion == "2":
                self.estrategia_actual = AtaqueFuerte()
                print("¡Has elegido un Ataque Fuerte!")
            else:
                self.estrategia_actual = AtaqueNormal()
                print("¡Has elegido un Ataque Normal!")

            
            dano_jugador = self.estrategia_actual.calcular_dano(self.jugador.ataque)
            self.enemigo.recibir_dano(dano_jugador)
            print(f"Atacas al {self.enemigo.nombre} y causas {dano_jugador} de daño.")

            
            if self.enemigo.vida > 0:
                
                dano_enemigo = AtaqueNormal().calcular_dano(self.enemigo.ataque)
                self.jugador.recibir_dano(dano_enemigo)
                print(f"El {self.enemigo.nombre} te ataca y causa {dano_enemigo} de daño.\n")
            
            turno_actual += 1

        self.determinar_ganador()

    def determinar_ganador(self):
        print("\n--- FIN DEL COMBATE ---")
        if self.jugador.vida > 0 and self.enemigo.vida == 0:
            print(f"¡El jugador ({self.jugador.nombre}) ha ganado!")
        elif self.enemigo.vida > 0 and self.jugador.vida == 0:
            print(f"¡El enemigo ({self.enemigo.nombre}) te ha derrotado!")
        else:
            print("El combate terminó en empate.")