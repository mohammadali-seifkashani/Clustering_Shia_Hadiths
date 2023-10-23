import re
from utils import load_json
from embedding import get_parts, get_max_part, tokenize_sentence, tokenize_word, tokenize_part


noor = load_json('../extra/noor_corrected.json')
not_in_data = set(load_json('not_in_data.json'))
myclustering = load_json('../results/maxcommonmax65.json')
myclustering = sorted(myclustering, key=lambda item: len(item), reverse=True)
data = load_json('../../data/hadiths_text3.json')

for i, mc in enumerate(myclustering):
    mc_set = set(mc)
    nc_corresponding_index = max(range(len(noor)), key=lambda i: len(mc_set.intersection(noor[i])))
    nc_corresponding = set(noor[nc_corresponding_index]) - not_in_data
    similarity = (len(nc_corresponding.intersection(mc_set)) - 1) / (len(nc_corresponding) - 1)
    notin = nc_corresponding - mc_set
    justin = mc_set - nc_corresponding

    if notin:
        for hn in notin:
            print(data[hn], hn)
        print()
    print(i)
    # for hn in justin:
    #     print(data[hn], hn)
    # print('\n**********************************************\n')
