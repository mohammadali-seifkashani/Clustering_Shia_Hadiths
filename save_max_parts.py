from time import time
from embedding import get_max_part
from utils import load_json, save_json


t = time()
data = load_json('../data/hadiths_text3.json')
# aye_texts = load_json('results/aye_texts.json')
idtokens = {}
for i, h in enumerate(data):
    mp = list(get_max_part(data[h]))
    if mp:
        idtokens[h] = mp
        print(i, len(data[h].split()), len(idtokens[h]))
idtokens = dict(sorted(idtokens.items(), key=lambda item: len(item[1])))
save_json(idtokens, '../data/idtokens.json')
print('time spent:', time() - t)
