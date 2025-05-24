import os
from PIL import Image


ASSETS_FOLDER = "assets"
BOARD_IMAGE = "board_optimized.png"
OUTPUT_IMAGE = "assets/final_board.png"
CELL_SIZE = 90


def generate_board_image():
    # test
    pieces_to_place = [
        ("checkmate.png", 0, 1),
        ("png_pieces/wK.png", 0, 1),
        ("png_pieces/bN.png", 1, 3),
    ]

    board_path = os.path.join(ASSETS_FOLDER, BOARD_IMAGE)
    board = Image.open(board_path).convert("RGBA")

    for piece_file, row, col in pieces_to_place:
        piece_path = os.path.join(ASSETS_FOLDER, piece_file)
        piece = Image.open(piece_path).convert("RGBA")
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        board.paste(piece, (x, y), mask=piece)

    board.save(OUTPUT_IMAGE)
    print(f"Board saved as {OUTPUT_IMAGE}")


if __name__ == "__main__":
    generate_board_image()
    print("Board image generation complete.")
