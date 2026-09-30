from facade import GameFacade

if __name__ == "__main__":
    print("Bienvenido al Videojuego por Turnos")
    print("Mundos disponibles:")
    print("1. Fantasia (Guerrero vs Dragón)")
    print("2. SciFi (Soldado vs Alien)")
    
    opcion = input("Elige tu mundo (1/2): ")
    mundo = "fantasia" if opcion == "1" else "scifi"
    
    
    juego = GameFacade(mundo)
    juego.jugar()