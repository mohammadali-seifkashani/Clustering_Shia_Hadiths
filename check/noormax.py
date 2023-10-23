import re
from utils import load_json, remove_all_tags
from embedding import tokenize_sentence, tokenize_word, get_parts, get_max_part, tokenize_part


noor = load_json('noor_automatic.json')
not_in_data = set(load_json('not_in_data.json'))
data = load_json('../../data/hadiths_text3.json')
idtokens = load_json('../../data/idtokens.json')
aye_texts = load_json('../results/aye_texts.json')

for i, nc in enumerate(noor):
    nc_set = set(nc) - not_in_data
    nc_seed = min(nc_set, key=lambda item: len(data[item].split()))
    nstokens = set(idtokens[nc_seed])
    for j, nh in enumerate(nc_set):
        nhtokens = set(idtokens[nh])
        similarity = len(nstokens.intersection(nhtokens)) * 2 / (len(nstokens) + len(nhtokens))
        if similarity < 0.45:
            print()
            print(data[nc_seed], similarity, nc_seed)
            print('############################################')
            print(data[nh], nh)
            print()
            break
    print(i)
