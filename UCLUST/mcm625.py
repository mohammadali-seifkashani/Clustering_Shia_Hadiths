from utils import load_json, save_json, time_decorator

# odd = ['421563', '409536', '232748', '357466']


def sort_seeds(set_tokenized, clusters, seeds):
    sorted_indices = sorted(
        range(len(clusters)),
        key=lambda i: len(set_tokenized.intersection(seeds[i]['set_tokenized'])) /
                      (len(set_tokenized) + len(seeds[i]['set_tokenized'])),
        reverse=True)
    return sorted_indices


def common_1_hadith(clusters, seeds, similarity_threshold, idtokens, hid):
    max_part = set(idtokens[hid])
    added_to_cluster = False
    sorted_indices = sort_seeds(max_part, clusters, seeds)

    for index in sorted_indices[:2]:
        seed, cluster = seeds[index], clusters[index]
        similarity = len(max_part.intersection(seed['set_tokenized'])) * 2 / (len(max_part) + len(seed['set_tokenized']))
        if similarity >= similarity_threshold:
            print('similarity:', similarity)
            cluster.append(hid)
            added_to_cluster = True
            # if len(seed['set_tokenized']) < len(max_part) <= len(seed['set_tokenized']) * 4 / 3:
            #     seeds[index] = {'hid': hid, 'set_tokenized': list(max_part)}
            #     cluster[-1], cluster[0] = cluster[0], cluster[-1]

    if not added_to_cluster:
        seeds.append({'hid': hid, 'set_tokenized': list(max_part)})
        clusters.append([hid])


@time_decorator
def greedy_clustering(data, sth, idtokens, seen):
    sthstr = int(100 * sth)

    d0 = data.popitem()
    while len(d0[1].split()) < 2:
       d0 = data.popitem()
    seeds = [{'hid': d0[0], 'set_tokenized': list(idtokens[d0[0]])}]
    clusters = [[d0[0]]]

    # clusters = load_json(f'../results/mcm{sthstr}.json')
    # seeds = load_json(f'../results/seedsofmcm{sthstr}.json')
    # for i in range(seen + 2):
    #     data.popitem()

    for i in range(len(data)):
        d = data.popitem()
        ds = d[1].split()
        if d[0] not in idtokens or not idtokens[d[0]] or len(ds) < 2:
            continue
        # if i == 364527:
        #     print()
        print(seen + i, len(ds), len(clusters))
        common_1_hadith(clusters, seeds, sth, idtokens, d[0])
        if i % 1000 == 0:
            print(f'******************************* SAVING {seen + i} ************************************')
            save_json(clusters, f'../results/mcm{sthstr}.json')
            save_json(seeds, f'../results/seedsofmcm{sthstr}.json')

    save_json(clusters, f'../results/mcm{sthstr}.json')
    return clusters


@time_decorator
def get_clustering_score(my_clustering, noor, not_in_data):
    sum_similarity = 0.
    count = 0

    for i, nc in enumerate(noor):
        nc_set = set(nc) - not_in_data
        if len(nc_set) < 2:
            continue
        count += 1
        mc_corresponding_index = max(range(len(my_clustering)), key=lambda i: len(nc_set.intersection(my_clustering[i])))
        mc_corresponding = my_clustering[mc_corresponding_index]
        similarity = (len(nc_set.intersection(mc_corresponding)) - 1) / (len(nc_set) - 1)
        sum_similarity += similarity
        print(i, len(nc_set), similarity)
        # notin = nc_set - set(mc_corresponding)
        # arein = nc_set - notin
        # if similarity < 0.8:
        #     print()

    return sum_similarity / count


data = load_json('../../data/hadiths_text3.json')
idtokens = load_json('../../data/idtokens.json')
similarity_threhsold = 0.625
seen = 0
myclustering = greedy_clustering(data, similarity_threhsold, idtokens, seen)
# myclustering = load_json('../results/mcm65.json')

noor = load_json('../check/noor_automatic.json')
not_in_data = set(load_json('../check/not_in_data.json'))
score = get_clustering_score(myclustering, noor, not_in_data)
print('len(clustering):', len(myclustering))
print('Score:', score)
