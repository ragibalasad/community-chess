from utils.pgn_engine import generate_board_image, validate_and_push_move, turn_to_play
import sys
import re


def update_readme(result):
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    value = turn_to_play()
    if result == "ongoing":
        pattern = rf"(<!-- START:turn -->)(.*?)(<!-- END:turn -->)"
        replacement = rf"\1 \nIt's team **{value}**'s turn to play \n\3"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    else:
        pattern = rf"(<!-- START:turn -->)(.*?)(<!-- END:turn -->)"
        replacement = rf"\1 \nGAME OVER! **{result}** {'won' if result in ['white', 'black'] else ''} \n\3"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("README updated with latest values.")


def main():
    san_move = sys.argv[1]
    result = validate_and_push_move(san_move)

    if result == "Illegal move.":
        print("That move is illegal!")
        return
    else:
        print("Move accepted and PGN updated.")

    generate_board_image()
    update_readme(result)

    if result != "ongoing":
        print(f"Game over: {result} {'won' if result in ['white', 'black'] else ''}")

    else:
        print("Game is still ongoing.")


if __name__ == "__main__":
    main()
