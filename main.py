from utils.pgn_engine import generate_board_image, validate_and_push_move, turn_to_play
import sys
import re


def update_readme(readme_path="README.md"):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections_to_update = {
        "turn": turn_to_play(),
        # You can add more sections here later, like:
        # "status": get_status_text(),
        # "moves": get_move_list(),
    }

    for key, value in sections_to_update.items():
        pattern = rf"(<!-- START:{key} -->)(.*?)(<!-- END:{key} -->)"
        replacement = rf"\1{value}\3"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("README updated with latest values.")


def main():
    # Example move input (replace with actual move input)
    san_move = sys.argv[1]

    # Validate and push the move in the PGN file
    result = validate_and_push_move(san_move)

    if result == "Illegal move.":
        print("That move is illegal!")
        return
    else:
        print("Move accepted and PGN updated.")
        print("Current FEN after move:", result)

    generate_board_image()
    update_readme()


if __name__ == "__main__":
    main()
