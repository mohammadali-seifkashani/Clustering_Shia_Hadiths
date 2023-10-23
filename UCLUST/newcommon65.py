import re
from utils import load_json, save_json, remove_all_tags
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer

mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
msa_d3_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='d3tok')


def tokenize_sentence(sentence):
    removed_tags = remove_all_tags(sentence)
    sub_sentence = re.sub('[░▀\\u200c\\u200dAHNOacefinoqrtuxz(){}<>«»^@#*+?,.؟!؛،:`_\-\d\'\"\\\[\]/]', '', removed_tags)
    tokenized_sentence = msa_d3_tokenizer.tokenize([sub_sentence])[0]
    return tokenized_sentence


def tokenize_part(part):
    result = []
    for word in part.split():
        if len(word) < 2:
            continue
        result.append(word)
        # splitted_tokenized = re.split('\+_|_\+|[ًٌٍَُِّْٰٖ]', word)
        # for w in splitted_tokenized:
        #     if len(w) < 2:
        #         continue
        #     result.append(w)
    return result


def get_hadith_parts(text):
    result = []
    tokenized_sentence = tokenize_sentence(text)
    # stopwords = {'اسناده', 'قلت', 'سالت', 'اساله','ابو عبد الله', 'ابي عبد الله', 'ابا عبد الله', 'عليه السلام', 'عليهما السلام', 'عليهم السلام', 'عز و جل', 'تعالي', 'جل و عز', 'جل اسمه', 'في قوله', 'صلي الله عليه و اله', 'روي', 'رواه', 'عن', 'اخرجه'}
    # tokenized_sentence = re.sub('|'.join(stopwords), '', tokenized_sentence)
    # textsplitted = re.split(':|قال', tokenized_sentence)
    textsplitted = re.split(':|قال|عز و جل|عليهم السلام|اخرجه|رواه|عن|روي|صلي الله عليه و اله|تعالي|عليه السلام|في قوله|جل اسمه|جل و عز|عليهما السلام|ابا عبد الله|ابي عبد الله|ابو عبد الله|سالت|اساله|قلت|اسناد', tokenized_sentence)
    for ts in textsplitted:
        tokens = tokenize_part(ts)
        if len(tokens) < 2:
            continue
        result.append(set(tokens))

    resultlen = len(result)
    for i in range(1, resultlen):
        result.append(result[i - 1] | result[i])

    if len(textsplitted) > 2:
        whole = set()
        for i in range(len(result)):
            whole.update(result[i])
        result.append(whole)

    return result


def sort_seeds(set_tokenized, clusters, seeds):
    sorted_indices = sorted(
        range(len(clusters)),
        key=lambda i: len(set_tokenized.intersection(seeds[i]['set_tokenized'])) /
                      (len(set_tokenized) + len(seeds[i]['set_tokenized'])),
        reverse=True)
    return sorted_indices


def common_1_hadith(clusters, seeds, similarity_threshold, hid, text):
    hadith_parts = get_hadith_parts(text)
    added_to_cluster = False
    # if hid in ['64602', '59543']:
        # print()

    for i, hpart in enumerate(hadith_parts):
        sorted_indices = sort_seeds(hpart, clusters, seeds)

        for index in sorted_indices[:5]:
            seed, cluster = seeds[index], clusters[index]
            similarity = len(hpart.intersection(seed['set_tokenized'])) * 2 / (len(hpart) + len(seed['set_tokenized']))
            if similarity >= similarity_threshold:
                print('similarity:', similarity)
                cluster.append(hid)
                added_to_cluster = True
                if len(seed['set_tokenized']) < len(hadith_parts[-1]) <= len(seed['set_tokenized']) * 4 / 3:
                    seeds[index] = {'hid': hid, 'set_tokenized': list(hadith_parts[-1])}

    if not added_to_cluster and hadith_parts and hadith_parts[-1]:
        seeds.append({'hid': hid, 'set_tokenized': list(hadith_parts[-1])})
        clusters.append([hid])


def greedy_clustering(data, sth, seen):
    sthstr = int(100 * sth)
    # d0 = data.popitem()
    # while len(d0[1].split()) < 2:
    #     d0 = data.popitem()
    # seeds = [{'hid': d0[0], 'set_tokenized': list(get_hadith_parts(d0[1])[-1])}]
    # clusters = [[d0[0]]]

    clusters = load_json(f'../results/common{sthstr}new.json')
    seeds = load_json(f'../results/seedsofcommon{sthstr}new.json')
    for i in range(seen + 2):
        data.popitem()

    for i in range(len(data)):
        d = data.popitem()
        print(seen + i, len(d[1].split()), len(clusters))
        common_1_hadith(clusters, seeds, sth, d[0], d[1])
        if i % 1000 == 0:
            print(f'******************************* SAVING {seen + i} ************************************')
            save_json(clusters, f'../results/common{sthstr}new.json')
            save_json(seeds, f'../results/seedsofcommon{sthstr}new.json')

    save_json(clusters, f'../results/common{sthstr}new.json')


data = load_json('../../data/hadiths_text3.json')
similarity_threhsold = 0.65
seen = 358000
greedy_clustering(data, similarity_threhsold, seen)
