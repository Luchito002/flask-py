from WinnerStatus import WinnerStatus

def print_tree(node, indent=0):
    if node is not None:
        # Asignar colores según el estado WinnerStatus
        if node.winner_status == WinnerStatus.WIN:
            winner_color = (0, 255, 0)
        elif node.winner_status == WinnerStatus.LOST:
            winner_color = (255, 0, 0)
        elif node.winner_status == WinnerStatus.DRAW:
            winner_color = (255, 255, 0)
        else:
            winner_color = (255, 255, 255) if indent % 2 == 0 else (0, 0, 255)  # Alternado

        color_str = f"\033[38;2;{winner_color[0]};{winner_color[1]};{winner_color[2]}m"
        reset_color = "\033[0m"

        print(f"{color_str}{'   ' * indent}{node.name}{reset_color}")

        if node.nodos:
            for child in node.nodos:
                print_tree(child, indent + 1)

