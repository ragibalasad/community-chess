from utils.pgn_engine import generate_board_image, validate_and_push_move, turn_to_play
import sys
import re
import json


def update_readme(result, username, san_move):
    with open("data/data.json") as f:
        data = json.load(f)

    if result == "Illegal move.":
        print(data["illegal_move"])
        return

    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update the badges section in README
    badges_pattern = rf"(<!-- START:badge_moves -->)(.*?)(<!-- END:badge_moves -->)"
    badges_replacement = rf"\1 \n![](https://img.shields.io/badge/Moves%20played-{data['moves_played']}-blue) \n\3"
    content = re.sub(badges_pattern, badges_replacement, content, flags=re.DOTALL)

    data["moves_played"] += 1
    with open("strings.json", "w") as f:
        json.dump(data, f, indent=4)

    badges_pattern = rf"(<!-- START:badge_games -->)(.*?)(<!-- END:badge_games -->)"
    badges_replacement = rf"\1 \n![](https://img.shields.io/badge/Completed%20games-{data['game_no'] - 1}-brightgreen) \n\3"
    content = re.sub(badges_pattern, badges_replacement, content, flags=re.DOTALL)

    num_players = len(data["players"])
    badges_pattern = rf"(<!-- START:badge_players -->)(.*?)(<!-- END:badge_players -->)"
    badges_replacement = rf"\1 \n![](https://img.shields.io/badge/Individual%20players-{num_players}-orange) \n\3"
    content = re.sub(badges_pattern, badges_replacement, content, flags=re.DOTALL)

    if username not in data["players"]:
        data["players"].append(username)
        with open("strings.json", "w") as f:
            json.dump(data, f, indent=4)

    # Update the issue section in README
    issue_pattern = rf"(<!-- START:issue -->)(.*?)(<!-- END:issue -->)"
    issue_replacement = rf"\1 \n[this issue](https://github.com/ragibalasad/ragibalasad/issues/{data['issue_no']})\3"
    content = re.sub(issue_pattern, issue_replacement, content, flags=re.DOTALL)

    # Update the turn section in README
    value = turn_to_play()
    if result == "ongoing":
        pattern = rf"(<!-- START:turn -->)(.*?)(<!-- END:turn -->)"
        replacement = rf"\1 \nIt's team **{value}**'s turn to play \n\3"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    else:
        pattern = rf"(<!-- START:turn -->)(.*?)(<!-- END:turn -->)"
        replacement = rf"\1 \nGAME OVER! **{result}** {'won' if result in ['white', 'black'] else ''} \n\3"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # update the most recent move section in README
    last_move_pattern = rf"(<!-- START:last_move -->)(.*?)(<!-- END:last_move -->)"
    last_move_replacement = rf"\1 \n**:alarm_clock: Most recent move:** `{san_move}` played by [@{username}](https://github.com/{username})\n\3"
    content = re.sub(last_move_pattern, last_move_replacement, content, flags=re.DOTALL)

    data["last_move_by"] = username
    with open("data/data.json", "w") as f:
        json.dump(data, f, indent=4)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("README updated with latest values.")


def main():
    username = sys.argv[1]
    san_move = sys.argv[2]
    result = validate_and_push_move(san_move)

    if result == "Illegal move.":
        print("That move is illegal!")
        return
    else:
        print("Move accepted and PGN updated.")

    generate_board_image()
    update_readme(result, username, san_move)

    if result != "ongoing":
        print(f"Game over: {result} {'won' if result in ['white', 'black'] else ''}")

    else:
        print("Game is still ongoing.")


if __name__ == "__main__":
    main()
