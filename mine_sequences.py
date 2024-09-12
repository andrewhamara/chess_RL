from prefixspan import PrefixSpan
import pandas as pd
import json

print('loading dataset')
data = pd.read_csv('/data/hamaraa/20k.csv')

print('preprocessing moves')
data['moves'] = data['moves'].apply(eval)

print('preprocssing material balance')
data['material_balance'] = data['material_balance'].apply(eval)
data.describe()

print('getting white wins')
white_wins = data[data['outcome'] == 1]['moves'].tolist()

print('getting black wins')
black_wins = data[data['outcome'] == -1]['moves'].tolist()

print('making white prefix span')
ps_white = PrefixSpan(white_wins)

print('getting white frequent')
white_sequences = ps_white.frequent(minsup=100)

print('getting white mined sequences')
white_mined_sequences = [seq[1] for seq in white_sequences if len(seq[1]) > 3]

print('making black prefix span')
ps_black = PrefixSpan(black_wins)

print('getting black frequent')
black_sequences = ps_black.frequent(minsup=100)

print('getting black mined sequences')
black_mined_sequences = [seq[1] for seq in black_sequences if len(seq[1]) > 3]

print('dumping white')
with open('white_mined.json', 'w') as f:
    json.dump(white_mined_sequences, f)
print('dumping black')
with open('black_mined.json', 'w') as f:
    json.dump(black_mined_sequences, f)
