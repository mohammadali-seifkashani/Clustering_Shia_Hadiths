# from tqdm import tqdm
from utils import load_json, time_decorator, save_json


@time_decorator
def merge(my_clustering, noor):
    result = []
    range_clustering = range(len(my_clustering))
    for i, nc in enumerate(noor):
        nc_set = set(nc)
        # if len(nc_set) <= 1:
        #     result.append(list(nc_set))
        #     continue
        mc_corresponding_index = max(range_clustering, key=lambda i: len(nc_set.intersection(my_clustering[i])))
        mc_corresponding = my_clustering[mc_corresponding_index]
        nc_set.update(mc_corresponding)
        result.append(list(nc_set))
        # similarity = (len(nc_set.intersection(mc_corresponding)) - 1) / (len(nc_set) - 1)
        print(i, end=',')

    return result


def do_merge_just_ids():
    print('loading data 30s ...')
    noor = load_json('noor_corrected.json')
    commonids = load_json('common_words_mean_70.json')
    print('len(clustering):', len(commonids))
    print('len(noor):', len(noor))
    merged = merge(commonids, noor)
    save_json(merged, '../data/merged_ids_common70.json')


def datahidtoi(data):
    result = {}
    for i, d in enumerate(data):
        result[d['hid']] = i
    return result


def ids_to_texts():
    result = []
    dumps_path = '/mnt/FAB8DBF0B8DBAA01/COMMON/my_projects/asgari/hadith_dumps/'
    data = load_json(dumps_path + 'all_texts_formatted.json')
    not_in_data = load_json('not_in_data.json')
    hid_i = datahidtoi(data)
    merged_ids_common70 = load_json('../data/merged_ids_common70.json')
    for j, cluster in enumerate(merged_ids_common70):
        text_cluster = []
        max_length = 0
        seed_hid = 0

        for i, hid in enumerate(cluster):
            if hid not in not_in_data:
                hadith = data[hid_i[hid]]
                if len(hadith['tokenized_text']) > max_length:
                    max_length = len(hadith['tokenized_text'])
                    seed_hid = hid
                text_cluster.append({'hid': hid, 'text': hadith['text']})

        for i, hadith in enumerate(text_cluster):
            if hadith['hid'] == seed_hid:
                text_cluster[i], text_cluster[0] = text_cluster[0], text_cluster[i]
                break

        result.append(text_cluster)
        print(j, end=',')

    save_json(result, '../data/merged_common70.json')


ids_to_texts()

