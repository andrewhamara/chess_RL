import pickle
import random
import chess

class ChessAgent:
    def __init__(self, env):
        self.env = env
        self.q_table = {}

    def choose_action(self, state, epsilon=0.5):
        legal_moves = list(self.env.board.legal_moves)

        if state not in self.q_table:
            self.q_table[state] = {move.uci(): 0 for move in legal_moves}

        if random.random() < epsilon:
            chosen_move = random.choice(legal_moves).uci()
        else:
            legal_q_values = {move: self.q_table[state].get(move.uci(), -float('inf')) for move in legal_moves}
            chosen_move = max(legal_q_values, key=legal_q_values.get).uci()

        if chosen_move not in self.q_table[state]:
            self.q_table[state][chosen_move] = 0

        return chosen_move

    def learn(self, state, action, reward, next_state):
        legal_moves = list(self.env.board.legal_moves)
        if state not in self.q_table:
            self.q_table[state] = {move.uci(): 0 for move in self.env.board.legal_moves}
        else:
            for move in legal_moves:
                if move.uci() not in self.q_table[state]:
                    self.q_table[state][move.uci()] = 0

        legal_moves_next = list(self.env.board.legal_moves)
        if next_state not in self.q_table:
            self.q_table[next_state] = {move.uci(): 0 for move in legal_moves_next}
        else:
            for move in legal_moves_next:
                if move.uci() not in self.q_table[next_state]:
                    self.q_table[next_state][move.uci()] = 0

        old_val = self.q_table[state][action]

        if self.q_table[next_state]:
            next_max = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0
        else:
            next_max = 0

        self.q_table[state][action] = old_val + 0.1 * (reward + 0.99 * next_max - old_val)

    def play(self, agent_color=chess.WHITE):
        state = self.env.reset()
        done = False

        while not done:
            action = self.choose_action(state)
            next_state, reward, done = self.env.step(action, agent_color)
            self.learn(state, action, reward, next_state)
            state = next_state
        return self.env.board.result()

    def save_agent(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f'Agent saved to {filename}')

    def load_agent(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)
        print(f'Agent loaded from {filename}')
