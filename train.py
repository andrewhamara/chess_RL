#!/usr/bin/env python3
import json
from environment import ChessEnvironment
from agent import ChessAgent
import chess

print('loading white mined sequences')
with open('/data/hamaraa/white_mined_uci.json', 'r') as f:
    white_mined_sequences = json.load(f)

print('loading black mined sequences')
with open('/data/hamaraa/black_mined_uci.json', 'r') as f:
    black_mined_sequences = json.load(f)

print('creating environment')
env = ChessEnvironment(white_sequences=white_mined_sequences, black_sequences=black_mined_sequences)

print('creating agent')
agent = ChessAgent(env)

print('starting training loop')
for episode in range(1000000):
    color = chess.WHITE if episode % 2 == 0 else chess.BLACK
    result = agent.play(agent_color=color)
    print(f"Game {episode + 1}: {result}")

filename = '/data/hamaraa/small_crazy.pkl'
print(f'Saving agent to {filename}')
agent.save_agent(filename)
