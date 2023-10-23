from utils import load_json, time_decorator, save_json


def get_hid_i(data):
    result = {}
    for i, d in enumerate(data):
        result[d['hid']] = i
    return result


def sort_seeds(set_tokenized_text, clusters_common, seeds_common):
    seeds_sorted, clusters_sorted = list(zip(*sorted(
        zip(seeds_common, clusters_common),
        key=lambda item: len(set_tokenized_text.intersection(item[0]['set_tokenized_text'])) /
                         (len(set_tokenized_text) + len(item[0]['set_tokenized_text'])),
        reverse=True
    )))
    return clusters_sorted, seeds_sorted


def common_1_hadith(clusters_common, seeds_common, similarity_threshold, d):
    set_tokenized_text = set(d['set_tokenized_text'])
    added_to_existing_cluster = False
    clusters_sorted, seeds_sorted = sort_seeds(set_tokenized_text, clusters_common, seeds_common)

    for i, (seed, cluster) in enumerate(zip(seeds_sorted[:5], clusters_sorted[:5])):
        similarity = len(set_tokenized_text.intersection(seed['set_tokenized_text'])) * 2 / \
                     (len(seed['set_tokenized_text']) + len(set_tokenized_text))
        if similarity >= similarity_threshold:
            print('similarity:', similarity, 'i\'th match:', i)
            cluster.append(d['hid'])
            added_to_existing_cluster = True

    if not added_to_existing_cluster:
        new_cluster = [d['hid']]
        seeds_common.append(d)
        clusters_common.append(new_cluster)


@time_decorator
def greedy_clustering(data, common_similarity_threhsold):
    # d0 = data.pop(0)
    # seeds_common = [d0]
    # clusters_common = [[d0['hid']]]
    hid_i = get_hid_i(data)
    clusters_common = load_json('../results/common70.json')
    seeds_common = [data[hid_i[cluster[0]]] for cluster in clusters_common]
    data = data[250002:]

    for i in range(len(data)):
        d = data.pop(0)
        if len(d['tokenized_text']) < 2:
            continue
        print(250002 + i, len(d['tokenized_text']), len(clusters_common))
        common_1_hadith(clusters_common, seeds_common, common_similarity_threhsold, d)
        if i % 50000 == 0:
            print(f'******************************* SAVING {i} ************************************')
            save_json(clusters_common, '../results/common70.json')

    save_json(clusters_common, '../results/common70.json')
    return clusters_common


data = load_json('../../data/new_hadiths_formatted.json')
common_similarity_threhsold = 0.7
clusters_common = greedy_clustering(data, common_similarity_threhsold)
