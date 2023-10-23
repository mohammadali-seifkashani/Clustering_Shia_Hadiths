import json
import re
from utils import load_json, time_decorator, save_json, remove_all_tags
from Bio import Align


aligner = Align.PairwiseAligner()
aligner.mode = "global"


def datahidtoi(data):
    result = {}
    for i, d in enumerate(data):
        result[d['hid']] = i
    return result


def get_alignments_method1(seq1: list, seq2: list):
    aligner.alphabet = seq1 + seq2
    aligned = aligner.align(seq1, seq2)
    return aligned[0][0], aligned[0][1]


def get_similarity_windows(t1, t2, mean_length):
    common_words = 0
    t1 = t1.replace('\'', '')
    t2 = t2.replace('\'', '')
    g1 = re.findall('\[[\w, ]+]|-+', t1)
    g2 = re.findall('\[[\w, ]+]|-+', t2)

    if len(g1) != len(g2):
        raise Exception
    for i in range(len(g1)):
        if g1[i] == g2[i]:
            common_words += g1[i].count(',') + 1
        elif '-' in g1[i] and g1[i].count('-') != g2[i].count(',') + 1:
            raise Exception
        elif '-' in g2[i] and g2[i].count('-') != g1[i].count(',') + 1:
            raise Exception

    return common_words / mean_length


def get_similarity_linux(t1, t2, mean_length):
    common_words = 0
    g1, g2 = t1, t2

    for i in range(len(g1)):
        if g1[i] == g2[i]:
            common_words += 1

    return common_words / mean_length


def get_bad_cluster(data, hid_i, cluster):
    print('BAD CLUSTER BAD CLUSTER BAD CLUSTER BAD CLUSTER BAD CLUSTER BAD CLUSTER ')
    print(json.dumps(cluster), ',')
    print_cluster(cluster, data, hid_i)


def print_cluster(cluster, data, hid_i):
    for hid in cluster:
        if hid in hid_i:
            hadith = data[hid_i[hid]]
            print({'hid': hadith['hid'], 'text': remove_all_tags(hadith['text'])})


@time_decorator
def merge(my_clustering, noor, hid_i, not_in_data):
    result = []
    range_clustering = range(len(my_clustering))
    faults = []
    for i, nc in enumerate(noor):
        nc_set = set(nc) - not_in_data
        uc_corresponding_index = max(range_clustering, key=lambda i: len(nc_set.intersection(my_clustering[i])))
        # uc_seed_id = my_clustering[uc_corresponding_index][0]
        # seed = data[hid_i[uc_seed_id]]['tokenized_text']
        uc_corresponding = set(my_clustering[uc_corresponding_index])
        noor_not_in_uc = nc_set - uc_corresponding
        uc_not_in_noor = uc_corresponding - nc_set

        # print(f'{i} noor_not_in_uc')
        # for hid in noor_not_in_uc:
        #     if hid not in not_in_data:
        #         aligned_seed, aligned_text = get_alignments_method1(seed, data[hid_i[hid]]['tokenized_text'])
        #         mean_length = (len(seed) + len(data[hid_i[hid]]['tokenized_text'])) / 2
        #         similarity = get_similarity_windows(aligned_seed, aligned_text, mean_length)
        #         print({'hid': hid, 'text': remove_all_tags(data[hid_i[hid]]['text']), 'similarity': similarity})

        # print()
        #
        # print(f'{i} uc_not_in_noor')
        for hid in uc_not_in_noor:
            # print({'hid': hid, 'text': remove_all_tags(data[hid_i[hid]]['text'])})
            bad_cluster = False
            for cluster in noor:
                if hid in cluster and len(cluster) != 1:
                    for ochid in cluster:
                        # print(ochid, ochid in uc_corresponding or ochid in not_in_data)
                        if not (ochid in uc_corresponding or ochid in not_in_data):
                            bad_cluster = True
                if bad_cluster:
                    faults.append(cluster)
                    get_bad_cluster(data, hid_i, cluster)
                    break

            if bad_cluster:
                break

        # print('\n**************************************************\n')

    save_json(faults, 'uclust_faults.json')
    return result


print('Loading data 30s ...')
dumps_path = 'C:/COMMON/my_projects/asgari/data/'
data = load_json(dumps_path + 'all_texts_formatted.json')
not_in_data = set(load_json('../data/not_in_data_before.json'))
hid_i = datahidtoi(data)
noor = load_json('noor_corrected.json')
ucids = load_json('../results/UCLUST_th55.json')
result = merge(ucids, noor, hid_i, not_in_data)
