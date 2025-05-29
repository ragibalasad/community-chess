import os
import chess
import chess.pgn
import svgwrite
import base64
from pathlib import Path

ASSETS_FOLDER = "assets"
PIECES_FOLDER = os.path.join(ASSETS_FOLDER, "svg_pieces")
OUTPUT_IMAGE = os.path.join(ASSETS_FOLDER, "final_board.svg")
CELL_SIZE = 90
BOARD_SIZE = CELL_SIZE * 8
PGN_PATH = os.path.join("data", "game.pgn")

PIECES = {
    "K": "wK.svg",
    "Q": "wQ.svg",
    "R": "wR.svg",
    "B": "wB.svg",
    "N": "wN.svg",
    "P": "wP.svg",
    "k": "bK.svg",
    "q": "bQ.svg",
    "r": "bR.svg",
    "b": "bB.svg",
    "n": "bN.svg",
    "p": "bP.svg",
}


def image_data_uri(path):
    """Return data URI of an SVG file"""
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/svg+xml;base64,{encoded}"


def load_board_from_pgn():
    if not os.path.exists(PGN_PATH):
        return chess.Board()

    with open(PGN_PATH, "r") as f:
        game = chess.pgn.read_game(f)
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
        return board


def save_board_to_pgn(board):
    game = chess.pgn.Game()
    node = game
    for move in board.move_stack:
        node = node.add_variation(move)
    with open(PGN_PATH, "w") as f:
        f.write(str(game))


def square_coords(square):
    file = chess.square_file(square)
    rank = 7 - chess.square_rank(square)
    return file * CELL_SIZE, rank * CELL_SIZE


def generate_board_image():
    board = load_board_from_pgn()
    dwg = svgwrite.Drawing(OUTPUT_IMAGE, size=(BOARD_SIZE, BOARD_SIZE))

    # Draw board squares
    colors = ["#f0d9b5", "#b58863"]
    for rank in range(8):
        for file in range(8):
            x = file * CELL_SIZE
            y = rank * CELL_SIZE
            fill = colors[(file + rank) % 2]
            dwg.add(dwg.rect(insert=(x, y), size=(CELL_SIZE, CELL_SIZE), fill=fill))

    # Highlight last move
    if board.move_stack:
        last_move = board.move_stack[-1]
        last_move_svg = os.path.join(PIECES_FOLDER, "last_move.svg")
        if os.path.exists(last_move_svg):
            data_uri = image_data_uri(last_move_svg)
            for square in [last_move.from_square, last_move.to_square]:
                x, y = square_coords(square)
                dwg.add(
                    dwg.image(href=data_uri, insert=(x, y), size=(CELL_SIZE, CELL_SIZE))
                )

    # Highlight check
    if board.is_check():
        king_square = board.king(board.turn)
        check_svg = os.path.join(PIECES_FOLDER, "check.svg")
        if os.path.exists(check_svg):
            data_uri = image_data_uri(check_svg)
            x, y = square_coords(king_square)
            dwg.add(
                dwg.image(href=data_uri, insert=(x, y), size=(CELL_SIZE, CELL_SIZE))
            )

    # Draw pieces
    for square, piece in board.piece_map().items():
        symbol = piece.symbol()
        filename = PIECES.get(symbol)
        if not filename:
            raise ValueError(f"Unknown piece symbol: {symbol}")
        filepath = os.path.join(PIECES_FOLDER, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Missing SVG: {filepath}")
        x, y = square_coords(square)
        data_uri = image_data_uri(filepath)
        dwg.add(dwg.image(href=data_uri, insert=(x, y), size=(CELL_SIZE, CELL_SIZE)))

    dwg.save()
    print(f"SVG board image saved at: {OUTPUT_IMAGE}")


def validate_and_push_move(move_str):
    board = load_board_from_pgn()
    try:
        move = board.parse_san(move_str)
    except ValueError:
        return "Illegal move."

    if move not in board.legal_moves:
        return "Illegal move."

    board.push(move)
    save_board_to_pgn(board)
    print("Move made successfully.")
    return board.fen()


if __name__ == "__main__":
    generate_board_image()
    # Example usage: validate_and_push_move("Kg4")
