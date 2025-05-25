import chess


try:
    with open("data/board_state.txt", "r") as f:
        board_state = f.read().strip()
        board = chess.Board(board_state)
except FileNotFoundError:
    board = chess.Board()


print(board)

pursed_comment = input("Enter your move in SAN format: ").strip()

try:
    board.push_san(pursed_comment)
    with open("data/board_state.txt", "w") as f:
        f.write(board.fen())
    print("Move made successfully.")
except ValueError as e:
    if "illegal san" in str(e).lower():
        print("Illegal move.")
    else:
        print(f"Error: {e}")

print("Check?" if board.is_check() else "No check.")
print("Current FEN:", board.fen())
