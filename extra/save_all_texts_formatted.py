import re
from utils import load_json, time_decorator, save_json, remove_all_tags
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tokenizers.morphological import MorphologicalTokenizer


def tokenize_sentence(sentence, msa_d3_tokenizer):
    sentence = remove_all_tags(sentence)
    result = []
    for word in re.split('[░▀\\u200c\\u200dAHNOacefinoqrtuxz(){}<>«»^@#*+?,.؟!؛،:`_\-\d\'\"\\\[\]/ ]', sentence):
        if len(word) < 2:
            continue
        tokenized_word = msa_d3_tokenizer.tokenize([word])[0]
        splitted_tokenized = re.split('\+_|_\+|[ًٌٍَُِّْٰٖ]', tokenized_word)
        for w in splitted_tokenized:
            if len(w) < 2:
                continue
            result.append(w)
    return result


@time_decorator
def tokenize_all(hadiths):
    mle_msa = MLEDisambiguator.pretrained('calima-msa-r13')
    msa_d3_tokenizer = MorphologicalTokenizer(disambiguator=mle_msa, scheme='d3tok')
    data = []

    for i, (hid, text) in enumerate(hadiths.items()):
        tokenized_text = tokenize_sentence(text, msa_d3_tokenizer)
        set_tokenized_text = list(set(tokenized_text))
        data.append({
            'hid': hid,
            'text': text,
            'tokenized_text': tokenized_text,
            'set_tokenized_text': set_tokenized_text
        })
        print(i, end=',')

    data = sorted(data, key=lambda item: len(item['tokenized_text']), reverse=True)
    return data


def save_text_of_ids():
    cl_till = load_json('../results/maxcommonmax65.json')
    data = load_json('../../data/hadiths_text3.json')
    result = []
    for cluster in cl_till:
        cluster_text = []
        for hid in cluster:
            cluster_text.append({'hid': hid, 'text': data[hid]})
        result.append(cluster_text)
    save_json(result, '../results/maxcommonmax65_texts.json')


save_text_of_ids()



def find_tags(text, aye_texts):
    text = re.sub('</?innocent>', ' ', text)
    tags = re.findall(r'<[^>]+>[^<>]+</[^>]+>', text)

    if tags and len(tags) % 2 == 0:
        for i in range(0, len(tags), 2):
            footnote = re.sub('(\])?<[^>]+>(\[)?', '', tags[i + 1])
            quranic = re.sub('(\])?<[^>]+>(\[)?', '', tags[i])
            quranic = re.sub('[░▀\\u200c\\u200dAHNOacefinoqrtuxz(){}<>«»^@#*+?,.؟!،؛`_\[\]/\-\d\'\"\\\:]', '', quranic).strip()
            if footnote in aye_texts and len(quranic) > len(aye_texts[footnote]):
                aye_texts[footnote] = quranic
            else:
                aye_texts[footnote] = quranic


def do_save_aye_texts():
    data = load_json('../../data/hadiths_text3.json')
    aye_texts = {}
    for i, (key, value) in enumerate(data.items()):
        editedchars = value.replace('اً', '').replace('ك', 'ک').replace('ي', 'ی').replace('ئ', 'ی').replace('أ', 'ا').replace('ؤ', 'و')
        without_erab = re.sub('[ًٌٍَُِّْٰ]', '', editedchars)
        find_tags(without_erab, aye_texts)
        print(i, end=',')
    save_json(aye_texts, '../results/aye_texts.json')

