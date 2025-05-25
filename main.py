from utils.pgn_engine import generate_board_image, validate_and_push_move


def main():
    # Example move input (replace with actual move input)
    san_move = input("Enter your move in SAN notation (e.g., e4, Nf3): ").strip()

    # Validate and push the move in the PGN file
    result = validate_and_push_move(san_move)

    if result == "Illegal move.":
        print("That move is illegal!")
    else:
        print("Move accepted and PGN updated.")
        print("Current FEN after move:", result)

    generate_board_image()


if __name__ == "__main__":
    main()
