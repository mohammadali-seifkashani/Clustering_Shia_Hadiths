import json
import time
import re


def time_decorator(func):
    def inner(*args, **kwargs):
        start_time = time.time()
        out = func(*args, **kwargs)
        spent_time = time.time() - start_time
        print("spent time:", spent_time)
        return out

    return inner


def save_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=3)


def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def remove_all_tags(text):
    # without_quranic = re.sub('<quranic_text>[^<>]+</quranic_text>', '', text)
    regex_all_tags = re.compile("<[^>]+>|\\n+")
    return re.sub(regex_all_tags, ' ', text)


def text_to_ids():
    result = []
    mm = load_json('extra/mmseqs2/mmseqs2_threshold55_0.json')
    mm += load_json('extra/mmseqs2/mmseqs2_threshold55_50000.json')
    mm += load_json('extra/mmseqs2/mmseqs2_threshold55_100000.json')
    mm += load_json('extra/mmseqs2/mmseqs2_threshold55_150000.json')
    mm += load_json('extra/mmseqs2/mmseqs2_threshold55_200000.json')
    mm += load_json('extra/mmseqs2/mmseqs2_threshold55_250000.json')
    mm += load_json('extra/mmseqs2/mmseqs2_threshold55_300000.json')
    mm += load_json('extra/mmseqs2/mmseqs2_threshold55_350000.json')
    mm += load_json('extra/mmseqs2/mmseqs2_threshold55_end.json')

    for i, cluster in enumerate(mm):
        result.append([h['hid'] for h in cluster])
        print(i, end=',')

    result = sorted(result, key=lambda item: len(item), reverse=True)
    save_json(result, 'extra/mmseqs2/mmseqs2_th55_ids.json')
    return result


# text_to_ids()
