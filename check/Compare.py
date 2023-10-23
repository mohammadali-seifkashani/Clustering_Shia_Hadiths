from utils import load_json, time_decorator, save_json


data = load_json('../../data/hadiths_text3.json')
# idtokens = load_json('../../data/idtokens.json')


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


noor = load_json('noor_automatic.json')
not_in_data = set(load_json('not_in_data.json'))
myclustering = load_json('../results/maxcommonmax35.json')
score = get_clustering_score(myclustering, noor, not_in_data)
print('len(clustering):', len(myclustering))
print('Score:', score)
