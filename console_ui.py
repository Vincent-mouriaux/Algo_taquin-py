import curses
from terminaltables import AsciiTable
from settings import PUZZLE_SIZE, GAME_TITLE
from controller import make_move, has_won


def init_ui():
    ui = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.noecho()
    ui.keypad(True)
    ui.nodelay(True)
    return ui

ui = init_ui()


def echo(data):
    """
    Utilitaire pour afficher une donnée à l'écran.
    Peut être utilisée pour afficher des informations de debug

    * data (str) : la donnée à afficher
    * ui (curse Window) : la UI sur laquelle afficher l'info
    """
    x = 10 + PUZZLE_SIZE * 2
    ui.addstr(x, 0, "%s  " % data)
    ui.refresh()


def handle_keypress(puzzle):
    try:
        key = ui.getkey().upper()
    except Exception:
        return puzzle

    height, width = ui.getmaxyx()

    if key == "KEY_DOWN":
        ui.addstr(height - 1, 0, "↓ DOWN - A FAIRE", curses.A_REVERSE)

        puzzle = make_move("DOWN", puzzle)

    elif key == "KEY_UP":
        ui.addstr(height - 1, 0, "↑ UP - A FAIRE", curses.A_REVERSE)
        puzzle = make_move("UP", puzzle)

    elif key == "KEY_LEFT":
        ui.addstr(height - 1, 0, "← LEFT - A FAIRE", curses.A_REVERSE)
        puzzle = make_move("LEFT", puzzle)

    elif key == "KEY_RIGHT":
        ui.addstr(height - 1, 0, "→ RIGHT - A FAIRE", curses.A_REVERSE)
        puzzle = make_move("RIGHT", puzzle)

    elif key in ("Q",):
        raise KeyboardInterrupt

    return puzzle


def get_puzzle_as_str(puzzle):
#    print(puzzle)
#    raise ValueError(str(puzzle))

    table = AsciiTable(puzzle)
    table.inner_heading_row_border = False
    table.inner_row_border = True
    table.justify_columns[0] = "center"
    table.justify_columns[1] = "center"
    return table.table


def display_output(puzzle):
    # Title
    ui.addstr(0, 0, GAME_TITLE, curses.color_pair(1))

    # Table game
    ui.addstr(2, 0, get_puzzle_as_str(puzzle), curses.color_pair(1))

    # Controls
    ui.addstr(4 + PUZZLE_SIZE * 2, 0, "Utiliser les flêches pour déplacer la case vide.")
    ui.addstr(5 + PUZZLE_SIZE * 2, 0, "(r)eset | (s)olution | (c)ancel | (q)uitter")

    if has_won(puzzle):
        ui.addstr(
            7 + PUZZLE_SIZE * 2,
            0,
            "🎉 🎺 🎺  V O U S   A V E Z   G A G N É   ! !  🎺 🎺 🎉",
            curses.color_pair(2) | curses.A_BLINK,
        )
    ui.refresh()


def clear_ui():
    curses.nocbreak()
    ui.keypad(False)
    curses.echo()
    curses.endwin()

