from WinnerStatus import WinnerStatus
from pintar_nodos import print_tree

ganadas = 0
perdidas = 0 
empatadas = 0
continuadas = 0

def verificar_ganador(tablero):
    global ganadas, perdidas, empatadas, continuadas
    # Condiciones de victoria
    lineas_ganadoras = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columnas
        [0, 4, 8], [2, 4, 6]              # Diagonales
    ]

    for linea in lineas_ganadoras:
        a, b, c = linea
        if tablero[a] and tablero[a] == tablero[b] == tablero[c]:
            if tablero[a] == "X":
                ganadas += 1
                return WinnerStatus.WIN

            perdidas += 1
            return WinnerStatus.LOST

    if all(casilla is not None for casilla in tablero):
        empatadas += 1
        return WinnerStatus.DRAW

    continuadas += 1
    return WinnerStatus.NONE

class Nodo:
    def __init__(self, name, isCheck, winner_status, nodos):
        self.name = name
        self.isCheck = isCheck
        self.winner_status = winner_status
        self.nodos = nodos

    def generar_arbol(self, tablero, jugador_actual):
        if self.isCheck:
            return

        for i in range(9):
            if tablero[i] is None:
                nuevo_tablero = tablero.copy()
                nuevo_tablero[i] = jugador_actual

                nuevo_estado = verificar_ganador(nuevo_tablero)

                nuevo_nodo = Nodo(
                    name=i,
                    isCheck=(nuevo_estado != WinnerStatus.NONE),
                    winner_status=nuevo_estado,
                    nodos=[]
                )

                self.nodos.append(nuevo_nodo)

                if nuevo_estado == WinnerStatus.NONE:
                    nuevo_nodo.generar_arbol(nuevo_tablero, 'O' if jugador_actual == 'X' else 'X')

def encontrar_movimiento_mas_cercano(nodo, status, message, camino_actual=None):
    if camino_actual is None:
        camino_actual = []

    if nodo.isCheck:
        if nodo.winner_status == status:
            return camino_actual + [nodo.name]
        else:
            return None

    caminos = []
    for hijo in nodo.nodos:
        camino_hijo = encontrar_movimiento_mas_cercano(hijo, status, message, camino_actual + [nodo.name])
        if camino_hijo is not None:
            caminos.append(camino_hijo)

    if len(caminos) == 0:
        return None

    # Devolver el camino más corto
    return min(caminos, key=len)

def movimiento_inmediato(posicion, tablero, status, jugador = "X"):
    tablero[posicion] = jugador
    if verificar_ganador(tablero) == status:
        return True
    return False



print(f"Número de veces ganadas: {ganadas}")
print(f"Número de veces perdidas: {perdidas}")
print(f"Número de veces empatadas: {empatadas}")
print(f"Número de veces que el juego continúa: {continuadas}")

def get_siguiente_movimiento(tablero):
    raiz = Nodo(name="inicio", isCheck=False, winner_status=None, nodos=[])
    raiz.generar_arbol(tablero, 'X')

    posicion = 0
    camino_ganador = encontrar_movimiento_mas_cercano(raiz, WinnerStatus.WIN, 'Con ganadores')
    camino_empate = encontrar_movimiento_mas_cercano(raiz, WinnerStatus.DRAW, 'Con empates')
    camino_perdedor = encontrar_movimiento_mas_cercano(raiz, WinnerStatus.LOST, 'Con perdedores')
    
    movimiento_inmediato_ganador = False
    movimiento_inmediato_empate = False
    movimiento_inmediato_perdedor = False
    
    if camino_ganador:
        movimiento_inmediato_ganador = movimiento_inmediato(camino_ganador[-1], tablero, WinnerStatus.WIN)
    if camino_empate:
        movimiento_inmediato_empate = movimiento_inmediato(camino_empate[-1], tablero, WinnerStatus.DRAW)
    if camino_perdedor:
        movimiento_inmediato_perdedor = movimiento_inmediato(camino_perdedor[-1], tablero, WinnerStatus.LOST, "O")
    
    if(camino_ganador is not None and movimiento_inmediato_ganador):
        return camino_ganador[-1]
    
    if(camino_empate is not None and movimiento_inmediato_empate):
        return camino_empate[-1]
    
    if(camino_perdedor is not None and movimiento_inmediato_perdedor):
        return camino_perdedor[-1]
    
    # No hay jugadas inmediatas
    if camino_ganador:
        return camino_ganador[-1]
    
    if camino_empate:
        return camino_empate[-1]
    
    if camino_perdedor:
        return camino_perdedor[-1]

    return posicion
