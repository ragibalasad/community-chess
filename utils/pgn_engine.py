import os
from PIL import Image
import chess
import chess.pgn
from io import StringIO

ASSETS_FOLDER = "assets"
BOARD_IMAGE = "board.png"
OUTPUT_IMAGE = os.path.join(ASSETS_FOLDER, "final_board.png")
CELL_SIZE = 90
PGN_PATH = os.path.join("data", "game.pgn")

PIECES = {
    "K": "wK.png",
    "Q": "wQ.png",
    "R": "wR.png",
    "B": "wB.png",
    "N": "wN.png",
    "P": "wP.png",
    "k": "bK.png",
    "q": "bQ.png",
    "r": "bR.png",
    "b": "bB.png",
    "n": "bN.png",
    "p": "bP.png",
}


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


def generate_board_image():
    board = load_board_from_pgn()

    board_image_path = os.path.join(ASSETS_FOLDER, BOARD_IMAGE)
    if not os.path.exists(board_image_path):
        raise FileNotFoundError(f"Board image not found: {board_image_path}")

    board_image = Image.open(board_image_path).convert("RGBA")

    # Highlight last move
    if board.move_stack:
        last_move = board.move_stack[-1]
        last_move_image_path = os.path.join(
            ASSETS_FOLDER, "png_pieces", "last_move.png"
        )
        if os.path.exists(last_move_image_path):
            last_move_image = Image.open(last_move_image_path).convert("RGBA")
            last_move_image = last_move_image.resize(
                (CELL_SIZE, CELL_SIZE), Image.LANCZOS
            )

            for square in [last_move.from_square, last_move.to_square]:
                x = chess.square_file(square) * CELL_SIZE
                y = (7 - chess.square_rank(square)) * CELL_SIZE
                board_image.paste(last_move_image, (x, y), mask=last_move_image)

    # Highlight check
    if board.is_check():
        king_square = board.king(board.turn)
        check_image_path = os.path.join(ASSETS_FOLDER, "png_pieces", "check.png")
        if os.path.exists(check_image_path):
            check_image = Image.open(check_image_path).convert("RGBA")
            check_image = check_image.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)

            x = chess.square_file(king_square) * CELL_SIZE
            y = (7 - chess.square_rank(king_square)) * CELL_SIZE
            board_image.paste(check_image, (x, y), mask=check_image)

    # Draw pieces
    for square, piece in board.piece_map().items():
        piece_symbol = piece.symbol()
        piece_filename = PIECES.get(piece_symbol)
        if not piece_filename:
            raise ValueError(f"Unknown piece symbol: {piece_symbol}")

        piece_image_path = os.path.join(ASSETS_FOLDER, "png_pieces", piece_filename)
        if not os.path.exists(piece_image_path):
            raise FileNotFoundError(f"Piece image not found: {piece_image_path}")

        piece_image = Image.open(piece_image_path).convert("RGBA")
        piece_image = piece_image.resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)

        x = chess.square_file(square) * CELL_SIZE
        y = (7 - chess.square_rank(square)) * CELL_SIZE
        board_image.paste(piece_image, (x, y), mask=piece_image)

    board_image.save(OUTPUT_IMAGE)
    print(f"Board image saved at: {OUTPUT_IMAGE}")


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
