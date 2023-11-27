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

def encontrar_resultados(nodos, status):
    resultados = []

    for nodo in nodos:
        if nodo.winner_status == status:
            resultados.append(nodo)

        resultados.extend(encontrar_resultados(nodo.nodos, status))

    return resultados

def siguiente_movimiento_computadora(nodos, tablero):
    tablero_actual = tablero.copy()

    ganadores = encontrar_resultados(nodos, WinnerStatus.WIN)
    if ganadores:
        for ganador in ganadores:
            tablero = tablero_actual.copy()
            tablero[ganador.name] = 'X'
            if verificar_ganador(tablero) == WinnerStatus.WIN:
                print("Movimiento de ganadores")
                return ganador.name

    perdedores = encontrar_resultados(nodos, WinnerStatus.LOST)
    if perdedores:
        for perdedor in perdedores:
            tablero = tablero_actual.copy()
            tablero[perdedor.name] = 'O'
            if verificar_ganador(tablero) == WinnerStatus.LOST:
                print(f"Movimiento de perdedores O con {perdedor.name}")
                return perdedor.name

    perdedores = encontrar_resultados(nodos, WinnerStatus.LOST)
    if perdedores:
        for perdedor in perdedores:
            tablero = tablero_actual.copy()
            tablero[perdedor.name] = 'X'
            if verificar_ganador(tablero) == WinnerStatus.LOST:
                print(f"Movimiento de perdedores O con {perdedor.name}")
                return perdedor.name

    empates = encontrar_resultados(nodos, WinnerStatus.DRAW)
    if empates:
        for empate in empates:
            tablero = tablero_actual.copy()
            tablero[empate.name] = 'X'
            if verificar_ganador(tablero) == WinnerStatus.DRAW:
                print("Movimiento de empates")
                return empate.name

    if ganadores:
        return ganadores[0].name

    for i in range(9):
        if tablero[i] is None:
            return i

# Imprimir información sobre el árbol
print(f"Número de veces ganadas: {ganadas}")
print(f"Número de veces perdidas: {perdidas}")
print(f"Número de veces empatadas: {empatadas}")
print(f"Número de veces que el juego continúa: {continuadas}")


def get_siguiente_movimiento(tablero):
    raiz_1 = Nodo(name="inicio", isCheck=False, winner_status=None, nodos=[])
    raiz_2 = Nodo(name="inicio", isCheck=False, winner_status=None, nodos=[])

    raiz_1.generar_arbol(tablero, 'X')
    raiz_2.generar_arbol(tablero, 'O')

    nodos = [raiz_2, raiz_1]

    posicion = siguiente_movimiento_computadora(nodos, tablero)
    #print_tree(raiz_1)  # Puedes elegir imprimir el árbol que prefieras
    return posicion
