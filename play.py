#!/usr/bin/env python3
import chess
from environment import ChessEnvironment
from agent import ChessAgent

class InferenceEnv:
    def __init__(self):
        self.board = chess.Board()

    def reset(self):
        self.board.reset()
        return self.board.fen()
    
    def step(self, action):
        while True:
            move = chess.Move.from_uci(action)
            if move in self.board.legal_moves:
                self.board.push(move)
                done = self.board.is_game_over()
                return self.board.fen(), done
            else:
                print("illegal move!")
                action = input("enter a new move: ")
    
    def render(self):
        print(self.board)

def play(agent, env):
    state = env.reset()
    done = False

    while not done:
        env.render()

        if env.board.turn == chess.WHITE:
            print('your turn {white):')
            move = input("enter your move in UCI format ")
            env.step(move)
        else:
            print("agent's turn (black):")
            action = agent.choose_action(state)
            state, done = env.step(action)

        if env.board.is_game_over():
            print('game over!')
            env.render()
            break

if __name__ == '__main__':
    print('creating environment')
    env = InferenceEnv()

    print('creating agent')
    agent = ChessAgent(env)
    agent.load_agent('/data/hamaraa/small.pkl')

    while True:
        play(agent, env)
        letter = input('q to quit, anything else to play again: ')
        if letter == 'q':
            break
