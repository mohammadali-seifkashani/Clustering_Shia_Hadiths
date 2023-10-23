from utils import load_json, save_json


noor = load_json('../check/noor_automatic.json')
not_in_data = set(load_json('../check/not_in_data.json'))
data = load_json('../../data/hadiths_text3.json')
idtokens = load_json('../../data/idtokens.json')
notinid = set(data.keys()) - set(idtokens.keys())
result = []

for i, nc in enumerate(noor):
    nc_set = set(nc) - not_in_data - notinid
    print(i, end=',')

    if len(nc_set) < 2:
        print(i, end=',')
        continue
    # elif 1 < len(nc_set) < 3:
    #     result.append(list(nc_set))
    #     print(i, end=',')
    #     continue

    nc_seed = min(nc_set, key=lambda item: len(data[item].split()))
    nstokens = set(idtokens[nc_seed])
    comparelist = list(nc_set - {nc_seed})

    for j, nh in enumerate(comparelist):
        nhtokens = set(idtokens[nh])
        similarity = len(nstokens.intersection(nhtokens)) * 2 / (len(nstokens) + len(nhtokens))

        if similarity <= 0.25:
            if len(nc_set) == 2:
                nc_set.pop()
                break

            if j == 0:
                chtokens = set(idtokens[comparelist[1]])
                similarity2 = len(nstokens.intersection(chtokens)) * 2 / (len(nstokens) + len(chtokens))

                if similarity2 <= 0.25:
                    bad = nc_seed
                    nc_set -= {bad}
                elif similarity2 >= 0.3:
                    bad = nh
                    nc_set -= {bad}

            else:
                bad = nh
                nc_set -= {bad}

            break

    if len(nc_set) > 1:
        result.append(list(nc_set))

save_json(result, '../check/noor_automatic.json')
