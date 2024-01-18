import random
from typing import List, Tuple

from flask import jsonify, Request


class TicTacToeGame:
    def __init__(self, board: List[List[str]]):
        self.board = board

    def check_win(self, player: str) -> bool:
        win_conditions = [
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[0][2], self.board[1][1], self.board[2][0]],
        ]
        return [player, player, player] in win_conditions

    def is_board_full(self) -> bool:
        return all(all(cell != " " for cell in row) for row in self.board)

    def make_move(self, action: int, player: str) -> str:
        row, col = divmod(action - 1, 3)
        self.board[row][col] = player

        if self.check_win(player):
            return f"Win for {player}"
        if self.is_board_full():
            return "Draw"
        return "Ongoing"

    def is_valid_move(self, action: int) -> bool:
        row, col = divmod(action - 1, 3)
        return 1 <= action <= 9 and self.board[row][col] == " "

    def update_game_state(self, action: int) -> Tuple[List[List[str]], str]:
        status = self.make_move(action, "O")
        if status == "Ongoing":
            empty_cells = [
                (r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "
            ]
            x_row, x_col = random.choice(empty_cells)
            self.board[x_row][x_col] = "X"
            status = self.make_move(x_row * 3 + x_col + 1, "X")
        return self.board, status


def play_game(request: Request):
    try:
        request_json = request.get_json(silent=True)
        if (
            not request_json
            or "board" not in request_json
            or "action" not in request_json
        ):
            return jsonify({"error": "Invalid input keys. Your request must contain 'board' and 'action' fields"}), 400

        board = request_json["board"]
        action = request_json["action"]

        if not isinstance(board, list) or not isinstance(action, int):
            return jsonify({"error": "Invalid input format. Your action must be integer."}), 400
        if len(board) != 3 or any(len(row) != 3 for row in board):
            return jsonify({"error": "Invalid board size. The size of the game board must be 3x3."}), 400
        if not all(cell in [" ", "O", "X"] for row in board for cell in row):
            return jsonify({"error": "Invalid board values. You can only use ' ', 'X', 'O."}), 400

        count_O = sum(row.count("O") for row in board)
        count_X = sum(row.count("X") for row in board)
        if count_O != count_X:
            return jsonify({"error": "Invalid board configuration: Number of 'O' and 'X' must be the same. Probably, you are mistakenly reflecting the player's actions on the board and sending a request. Please note the board's information must not reflect user's current action."}), 400


        game = TicTacToeGame(board)

        if not game.is_valid_move(action):
            return jsonify({"error": "Invalid Move. Please select a blank cell for an action."}), 400

        updated_board, game_status = game.update_game_state(action)

        return jsonify({"board": updated_board, "status": game_status})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
