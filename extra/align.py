from utils import save_json, load_json, time_decorator, remove_all_tags
from Bio import Align
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer
import re


aligner = Align.PairwiseAligner()
aligner.mode = "global"


def tokenize_sentence(sentence, msa_d3_tokenizer):
    sentence = remove_all_tags(sentence)
    without_erab = re.sub('[ًٌٍَُِّْٰ]', '', sentence)
    result = []
    for word in re.split('[░▀\\u200c\\u200dAHNOacefinoqrtuxz(){}<>«»^@#*+?,.؟!؛،:`_\-\d\'\"\\\[\]/ ]', without_erab):
        if len(word) < 2:
            continue
        tokenized_word = msa_d3_tokenizer.tokenize([word])[0]
        splitted_tokenized = re.split('\+_|_\+', tokenized_word)
        for w in splitted_tokenized:
            if len(w) < 2:
                continue
            result.append(w)
    return result


def get_alignments(seq1: list, seq2: list):
    aligner.alphabet = set(seq1 + seq2)
    aligned = aligner.align(seq1, seq2)
    return aligned[0][0], aligned[0][1]


@time_decorator
def alignall():
    clusters = load_json('../results/maxcommonmax65.json')
    # data = load_json('../../data/hadiths_text3.json')
    # mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
    # msa_d3_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='d3tok')
    # hids = set()
    # for cluster in clusters:
    #     hids.update(cluster)
    # tokens = {}
    # for i, hid in enumerate(hids):
    #     tokens[hid] = tokenize_sentence(data[hid], msa_d3_tokenizer)
    #     print(i, end=',')
    # save_json(tokens, '../results/tokens65.json')
    tokens = load_json('../results/tokens65.json')

    alignments = []

    for i, cluster in enumerate(clusters):
        seedid = cluster.pop(0)
        if seedid not in tokens:
            continue
        seed_tokens = tokens[seedid]
        if not len(cluster):
            alignments.append(seed_tokens)
            continue
        cluster_alignments = []
        for hid in cluster:
            if hid not in tokens:
                continue
            h_tokens = tokens[hid]
            a1, a2 = get_alignments(seed_tokens, h_tokens)
            cluster_alignments.append([a1, a2])
        alignments.append(cluster_alignments)
        print(i, end=',')

    save_json(alignments, '../results/mcm65aligns.json')
    return alignments


alignments = alignall()
