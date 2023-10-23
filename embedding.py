import re
from utils import load_json, remove_all_tags

extrawords = {'هما', 'الی'}


# def replace_quranic(text):
#     text = re.sub('</?innocent>', ' ', text)
#     tags = re.findall(r'<[^>]+>[^<>]+</[^>]+>', text)
#
#     if tags and len(tags) % 2 == 0:
#         for i in range(0, len(tags), 2):
#             quranic = re.sub('(\])?<[^>]+>(\[)?', '', tags[i])
#             footnote = re.sub('(\])?<[^>]+>(\[)?', '', tags[i + 1])
#             text = text.replace(f'<footnote>[{footnote}]</footnote>', ' ')
#             text = text.replace(f'<quranic_text>{quranic}</quranic_text>', aye_texts[footnote])
#
#     return text


def tokenize_sentence(text):
    removed_tags = remove_all_tags(text)
    edited_chars = removed_tags.replace('اً', 'ا').replace('ك', 'ک').replace('ي', 'ی').replace('ئ', 'ی').replace('أ', 'ا').replace('ؤ', 'و')
    without_erab = re.sub('[ًٌٍَُِّْٰ]', '', edited_chars)
    # removed_tags = replace_quranic(without_erab, aye_texts)
    sub_sentence = re.sub('[░▀\\u200c\\u200dAHNOacefinoqrtuxz(){}<>«»^@#*+?,.؟!،؛`_\[\]/\-\d\'\"\\\]', ' ', without_erab)
    removingwords = ['فی الحسن', r'جزا\w الله \w+ (خیرا)?', 'شیخ ', 'امیر ال', 'ابی طالب', 'ابن عباس', 'علیه الصلاة و السلام', 'و الذی بعث\w+ بالحق', 'سبحان', 'یعنی', '(الله)? صلی الله علیه( و اله)?( و سلم)?', '(تبارک و )?تعالی', 'علیه (الصلاة و )?السلام', 'علیها السلام', 'علیهما السلام', 'علیهم السلام', 'سلام الله علیه', 'عز و جل', 'جل اسمه', 'جل و عز', 'و علی الایمة من ولده', 'صلوات الله علی(ه)?( و اله)?']
    re_tokenized = re.sub('|'.join(removingwords), ' ', sub_sentence)
    return re_tokenized


def tokenize_part(part):
    result = []
    if part:
        for pw in part.split():
            if len(pw) < 2 or pw in extrawords:
                continue
            tokenized_words = tokenize_word(pw)
            result += [tw for tw in tokenized_words if len(tw) > 1 and tw not in extrawords]
    return result


def tokenize_word(word):
    extra = []
    if re.match(r'\bال\w+', word) and word not in ['الله', 'التی', 'الی'] and not word.startswith('الذی'):
        word = word[2:]
    elif re.match(r'بال\w+', word):
        word = word[3:]
    elif re.match(r'ب\w+', word) and not word in ['بر'] and not any(word.startswith(b) for b in ['بعث', 'بن', 'بعد', 'بین', 'بلغ', 'بیت', 'باع', 'باب', 'بلی']):
        word = word[1:]
    elif re.match(r'فل\w+', word):
        word = word[2:]
    elif re.match(r'ف\w+', word) and word not in ['فاطمة', 'فریضة'] and not any(word.startswith(b) for b in ['فطر', 'فضل', 'فی', 'فوق', 'فخر', 'فتح']):
        word = word[1:]
    elif re.match(r'لل\w+', word) and word not in ['لله']:
        word = word[2:]
    elif re.match(r'ل\w+', word) and word not in ['لوح', 'لحم'] and not re.match(r'لعن((?!اء\b)\w*)', word) and not any(word.startswith(b) for b in ['لیل', 'لسان', 'لعل', 'لیل', 'لست']) or word == 'لعلی':
        word = word[1:]

    if re.match(r'\w+نا\b', word) and word not in ['انا', 'هاهنا', 'مومنا', 'اثنا', 'منا', 'اعانا']:
        word = word[:-2]
        extra.append('نا')

    if re.match(r'\w+هما\b', word):
        word = word[:-3]
        extra.append('هما')
    elif re.match(r'\w+کما\b', word):
        word = word[:-3]
        extra.append('کما')
    elif re.match(r'\w+کم\b', word):
        word = word[:-2]
        extra.append('کم')
    elif re.match(r'\w+هم\b', word) and word not in ['اللهم']:
        word = word[:-2]
        extra.append('هم')
    elif re.match(r'\w+ها\b', word) and word not in ['کرها', 'ایتها', 'ایها']:
        word = word[:-2]
        extra.append('ها')
    elif re.match(r'\w+ک\b', word) and not any(word.endswith(b) for b in ['ذلک', 'ملک', 'تلک', 'مسک']):
        word = word[:-1]
    elif re.match(r'\w+ه\b', word) and word not in ['الله', 'هذه', 'علیه', 'شبه', 'شبیه', 'مطیه', 'کره', 'سجده']:
        word = word[:-1]
    elif re.match(r'\w+[^و]ا\b', word) and word not in ['لا', 'هذا', 'اقضا', 'اذا', 'اثنا', 'انا', 'ایها', 'ایتها', 'رضا'] and not word.endswith('کذا'):
        word = word[:-1]

    if word[0] == 'ی' and not any(word.startswith(b) for b in ['ید', 'یوم']):
        word = word[1:]
    elif word[0] == 'ت' and not any(word.startswith(b) for b in ['تاب', 'تار']):
        word = word[1:]

    return [word] + extra


def get_parts(text):
    preresult = []
    tokenized_sentence = tokenize_sentence(text)
    splittingwords = [r'\bسنة (?!فی\b)\w+ (\w+ )?و \w+', r'سالت (\w+ ){,5}عن', 'متفق علی صحت', 'حدیث', 'من طرق', 'عکبری', 'کتاب السنن',
                      r'علی حد \w+ الکتاب', r'من \w+ طرق', r'\W?\bعن ', 'اخرجه',
                      'رواه', 'روی', ':', 'قال', 'قوله ', 'فی قول', 'سالت', 'اساله', 'اسناد', ' بن ', r'ابن ((?!مریم\b)\w+)',
                      'حدثن', 'ترمذی', 'سجستانی', 'بخاری', 'حنبل', r'ابو (\w+)?', 'ابی', 'فی کتاب', 'فی باب', 'التمیمی',
                      'مروزی', 'ذکره', 'ذکرنا', 'سمعت', 'انبان', 'اخبرن', 'املاء', 'روای(ة|ت)', 'موصلی', 'سمعانی', 'عامری', 'عشاری',
                      'رازی', 'نیسابوری', 'شیبانی', 'قطان', 'خباز', 'خلال', 'هروی', 'قزوینی', 'مثل ذلک', 'عبد الملک',
                      'هاشمی', 'قلت', 'فوارس', 'اعرج', 'نسابة', 'حایریة', 'موسوی', 'حلبی', 'راوندی', 'سکری', 'سنده'
                      r'خط (\w+ ){1,3}\s*ب', 'کلدة', 'راوی', r'قراء(ة|ت)(\w)?', 'مایة', r'فی \w+ سند', 'قول', ' بل ',
                      'همدانی', 'خوارزمی', 'حسینی', 'ذکرت', 'اخطب', 'مرتضی', 'ادیب', r'\bعبد ', 'ازجی', ' صفر ', 'صحاح',
                      r'\bام ', r'[^ل]رجال', 'اسفرایینی', 'رووا', 'مسیری', 'قیس', 'واسطی', 'رایت', 'رابع', 'مسند', 'ابانة'
                      ' اخذ(\w*)', r'روای(ا)?ت', 'قیصر', 'تاریخ', 'ارقم', 'سریحة', 'اهل الشورا', 'احتجاجه', 'برقی',
                      'من (\w+) طرق', 'جعانی', 'من طریقین', 'شرف المصطفی']
    splittingregex = '|'.join(splittingwords)
    textsplitted = re.split(splittingregex, tokenized_sentence)

    for ts in textsplitted:
        tokens = set(tokenize_part(ts)) - {'ال'}
        if tokens:
            preresult.append(tokens)
    return preresult


def get_max_part(text):
    parts = get_parts(text)
    end = re.findall(r':[^:.]+\.$', text)

    result = set()
    if end:
        endparts = get_parts(end[-1])
        for ep in endparts:
            result.update(ep)

    if not parts:
        return result

    goodpart = 0
    for p in parts:
        if len(p) >= 3:
            result.update(p)
            goodpart += 1
    if goodpart == 0 or (goodpart == 1 and len(result) < 4):
        sorted_parts = sorted(parts[::-1], key=lambda item: len(item), reverse=True)
        twomax = sorted_parts[:2]
        if len(twomax) == 1:
            return set(twomax[0])
        else:
            return set(twomax[0]) | set(twomax[1])
    else:
        return result

# r'و ال\w+ فی ال((?!له\b)\w+)'
# r'\[[^\] ]+\]', '\[', '\]'
