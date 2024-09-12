import chess
import hashlib
import json

def hash_sequence(sequence):
    sequence_str = ''.join(sequence)
    return hashlib.md5(sequence_str.encode('utf-8')).hexdigest()

def load_hashed_sequences(file_path):
    with open(file_path, 'r') as f:
        sequences = json.load(f)
    hashed_sequences = {hash_sequence(seq): seq for seq in sequences}
    return hashed_sequences

class ChessEnvironment:
    def __init__(self, white_sequences, black_sequences):
        self.board = chess.Board()
        self.white_sequences = white_sequences
        self.black_sequences = black_sequences
        self.hashed_black_sequences = load_hashed_sequences('/data/hamaraa/white_mined_uci.json')
        self.hashed_white_sequences = load_hashed_sequences('/data/hamaraa/black_mined_uci.json')

    def reset(self):
        self.board.reset()
        return self.board.fen()

    def step(self, action, agent_color):
        move = chess.Move.from_uci(action)
        if self.board.is_legal(move):
            self.board.push(move)
            reward = self.get_reward(agent_color)
            done = self.board.is_game_over()
            return self.board.fen(), reward, done

    def get_reward(self, agent_color):
        piece_values = {
                chess.PAWN: 1,
                chess.KNIGHT: 3,
                chess.BISHOP: 3.5,
                chess.ROOK: 6,
                chess.QUEEN: 10,
                chess.KING: 0
        }
        current_game = [move.uci() for move in self.board.move_stack]
        reward = 0

        cur_hash = hash_sequence(current_game)

        if self.board.is_checkmate():
            reward = 100 if self.board.turn != agent_color else -100
            return reward

        if self.board.turn == chess.WHITE:
            hash_sequences = self.hashed_white_sequences
        else:
            hash_sequences = self.hashed_black_sequences

        if cur_hash in hash_sequences:
            print('WAWAWAWAWAWAWAWA')
            reward += 100

        material_reward = 0
        for piece in self.board.piece_map().values():
            material_reward += piece_values.get(piece.piece_type, 0) * (1 if piece.color == chess.WHITE else -1)

        reward += material_reward / 100

        if self.board.is_stalemate() or self.board.is_insufficient_material():
            reward -= 50

        return reward

    def render(self):
        print(self.board)
