import os
from PIL import Image
import chess

ASSETS_FOLDER = "assets"
BOARD_IMAGE = "board.png"
OUTPUT_IMAGE = os.path.join(ASSETS_FOLDER, "final_board.png")
CELL_SIZE = 90

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


def generate_board_image():
    board_txt_path = os.path.join("data", "board_state.txt")
    if not os.path.exists(board_txt_path):
        raise FileNotFoundError(f"Missing board_state.txt at {board_txt_path}")

    with open(board_txt_path, "r") as f:
        board_state = f.read().strip()

    if not board_state:
        raise ValueError("board.txt is empty")

    board = chess.Board(board_state)
    if not board.is_valid():
        raise ValueError("Invalid board state in board.txt")

    board_image_path = os.path.join(ASSETS_FOLDER, BOARD_IMAGE)
    if not os.path.exists(board_image_path):
        raise FileNotFoundError(f"Board image not found: {board_image_path}")

    board_image = Image.open(board_image_path).convert("RGBA")

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


if __name__ == "__main__":
    generate_board_image()
