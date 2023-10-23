import re
from utils import save_json, time_decorator, load_json
from Bio import Align


aligner = Align.PairwiseAligner()
aligner.mode = "global"


def get_hid_i(data):
    result = {}
    for i, d in enumerate(data):
        result[d['hid']] = i
    return result


def sort_seeds(clusters_uclust, seeds_uclust, set_tokenized_text):
    seeds_sorted, clusters_sorted = list(zip(*sorted(
        zip(seeds_uclust, clusters_uclust),
        key=lambda item: len(set_tokenized_text.intersection(item[0]['set_tokenized_text'])) /
                         (len(set_tokenized_text) + len(item[0]['set_tokenized_text'])),
        reverse=True
    )))
    return clusters_sorted, seeds_sorted


def get_alignments(seq1: list, seq2: list):
    aligner.alphabet = seq1 + seq2
    aligned = aligner.align(seq1, seq2)
    return aligned[0][0], aligned[0][1]

print()
def get_similarity_linux(t1, t2, mean_length):
    common_words = 0
    g1, g2 = t1, t2

    for i in range(len(g1)):
        if g1[i] == g2[i]:
            common_words += 1

    return common_words / mean_length


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


def uclust_main(clusters_uclust, seeds_uclust, similarity_threshold, d):
    set_tokenized_text = set(d['set_tokenized_text'])
    clusters_sorted, seeds_sorted = sort_seeds(clusters_uclust, seeds_uclust, set_tokenized_text)
    added_to_existing_cluster = False

    for i, (seed, cluster) in enumerate(zip(seeds_sorted[:5], clusters_sorted[:5])):
        aligned_seed, aligned_text = get_alignments(seed['tokenized_text'], d['tokenized_text'])
        mean_length = (len(seed['tokenized_text']) + len(d['tokenized_text'])) / 2
        similarity = get_similarity_linux(aligned_seed, aligned_text, mean_length)
        if similarity >= similarity_threshold:
            print('similarity:', similarity, "i'th match:", i + 1)
            cluster.append(d['hid'])
            added_to_existing_cluster = True

    if not added_to_existing_cluster:
        new_cluster = [d['hid']]
        seeds_uclust.append(d)
        clusters_uclust.append(new_cluster)


@time_decorator
def greedy_clustering(data, uclust_similarity_threshold):
    d0 = data.pop(0)
    seeds_uclust = [d0]
    clusters_uclust = [[d0['hid']]]
    # hid_i = get_hid_i(data)
    # clusters_uclust = load_json('../results/UCLUST70new.json')
    # seeds_uclust = [data[hid_i[cluster[0]]] for cluster in clusters_uclust]
    # data = data[250002:]

    for i in range(len(data)):
        d = data.pop(0)
        if len(d['tokenized_text']) < 2:
            continue
        print(i, len(d['tokenized_text']), len(clusters_uclust))
        uclust_main(clusters_uclust, seeds_uclust, uclust_similarity_threshold, d)

        if i % 50000 == 0:
            print(f'******************************* SAVING {i} ************************************')
            save_json(clusters_uclust, '../results/UCLUST70new.json')

    save_json(clusters_uclust, '../results/UCLUST70new.json')
    return clusters_uclust


data = load_json('../../data/new_hadiths_formatted.json')
sth = 0.7
greedy_clustering(data, sth)
