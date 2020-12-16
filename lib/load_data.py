import re
import json
from lxml import etree
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial
from itertools import compress


LINK = '(http|https)://[가-힣a-zA-Z0-9\./=#_%~&\-\?:;\(\)]+'


def kowiki_sentences(path, mode='kowiki-sens-kor'):
    contents = []
    c_append = contents.append
    for _, e in tqdm(etree.iterparse(path)):
        etag = e.tag.split('}')[-1]
        if etag == 'text':
            c_append(preprocessing(e.text, mode=mode))
        e.clear()
    contents = list(compress(contents,contents))
    return contents


def korquad1_sentences(path, num_cores, mode='korquad1-sens-kor'):
    contents = load_json(path)
    contents = get_korquad1_sentences(contents)
    func = partial(preprocessing, mode=mode)
    contents = run_imap_multiprocessing(func, contents, num_cores)
    return contents


def korquad2_sentences(path, num_cores, mode='korquad2-sens-kor'):
    contents = load_json(path)
    contents = list(map(lambda x: x['context'], contents['data']))
    func = partial(preprocessing, mode=mode)
    contents = run_imap_multiprocessing(func, contents, num_cores)
    contents = list(compress(contents,contents))
    return contents


def namuwiki_sentences(path, num_cores, mode='namuwiki-sens-kor'):
    contents = load_json(path)
    contents = list(map(lambda x:x['text']+'\n\n', contents))
    func = partial(preprocessing, mode=mode)
    contents = run_imap_multiprocessing(func, contents, num_cores)
    return contents


def get_korquad1_sentences(dict_korquad):
    output = []
    append = output.append
    for data in dict_korquad['data']:
        for paragraph in data['paragraphs']:
            append(paragraph['context'])
            append('')
            for qa in paragraph['qas']:
                append(qa['question'])
                append('')
                for ans in qa['answers']:
                    append(ans['text'])
                    append('')
    return output


def load_json(path):
    with open(path, 'r', encoding='utf-8') as r:
        contents = json.load(r)
    return contents


def run_imap_multiprocessing(func, argument_list, num_processes):

    pool = Pool(processes=num_processes)

    result_list_tqdm = []
    for result in tqdm(pool.imap(func=func, iterable=argument_list), total=len(argument_list)):
        result_list_tqdm.append(result)

    return result_list_tqdm


def preprocessing(content, mode='kowiki-sens-kor'):
    if not isinstance(content, str):
        return content
    if mode == 'kowiki-sens-kor':
        pairs = [['<', '>'], ['{{', '}}'], ['{', '}']]
        for f, l in pairs:
            content = remove_with_inside(content, f, l)
        content = re.sub('{}', '', content)

        replace_char = [["\'{2,}", "\'"], ['\"{2,}', '\"']]
        for key, value in replace_char:
            content = re.sub(key, value, content)

        rm_patterns = ['(?<=\n)[ :;#\*\-]+',
                       '(?<=\[\[)[^\[]+\|(?=[^\|\]]+\]\])',
                       '[\[\]]{2,}', "={2,}", LINK, '\[\]',
                       '(?<=\n)\'+', '(?<=\n)/+', '(?<=\n) +', '\(, \)']

        for pattern in rm_patterns:
            content = re.sub(pattern, '', content)

        content = '\n'.join(list(filter(
            lambda x: len(x.split()) > 3 and re.compile('[가-힣]').match(x),
            content)))

        rm_patterns = ['(?<=\n)[^가-힣]+(?=\n)', '(?<=\n)\[.+\](?=\n)', '(?<=[ 가-힣])[\[\]](?=[ 가-힣])']
        for pattern in rm_patterns:
            content = re.sub(pattern, '', content)

        content = re.sub('\n{2,}','\n\n', content)

    elif mode == 'namuwiki-sens-kor':
        pairs =[['<', '>'],['{{', '}}'],['{', '}'],['~~', '~~']]
        for f,l in pairs:
            content = remove_with_inside(content,f, l)
        content = re.sub('{}', '', content)

        replace_char = [["\'{2,}", "\'"], ['\"{2,}', '\"']]
        for key, value in replace_char:
            content = re.sub(key, value, content)

        rm_patterns = ['(?<=\n)[ :;#\*\-]+',
                       '(?<=\[\[)[^\[]+\|(?=[^\|\]]+\]\])',
                       '[\[\]]{2,}', '={2,}', LINK, '\[\]',
                       '(?<=\n)[\'/ ▲>]+', '\(, \)',
                       '(?<=\n)[^가-힣]+(?=\n)', '(?<=\n)\[.+\](?=\n)',
                       '(?<=\n)\|.+\|(?=\n)', '\[\*.+\]']
        for pattern in rm_patterns:
            content = re.sub(pattern, '', content)

        sentences = []
        for c in content.split('\n'):
            if (len(c.split()) > 3 and re.compile('[가-힣]').match(c)) or (c == ''):
                sentences+=c
        content = '\n'.join(sentences)
        content = re.sub('\n{2,}', '\n\n', content)
        content = re.sub('(?<=\n)파일:[^\n]+', '', content)

    elif mode == 'korquad1-sens-kor':
        return content
    elif mode =='korquad2-sens-kor':
        content = remove_with_inside(content, '<', '>', padding='')

        rm_patterns = [LINK,'\[편집\]', '(?<=\n)[↑\-]', '(?<=\n)분류:.+(?=\n)', '(?<=[ 가-힣])[\[\]](?=[ 가-힣])']
        for pattern in rm_patterns:
            content = re.sub(pattern, '', content)

        sentences = []
        for c in content.split('\n'):
            if (len(c.split()) > 3 and re.compile('[가-힣]').match(c)) or (c==''):
                sentences.append(c)
        content = '\n'.join(sentences)
        rm_patterns = ['(?<=[ 가-힣])[\[\]](?=\n)', '\[[0-9]+\](?=\n)']
        for pattern in rm_patterns:
            content = re.sub(pattern, '', content)
        content = re.sub('\n{2,}', '\n\n', content)
    else:
        raise KeyError('해당 키에 대한 방법이 정의되어 있지 않습니다.')
    return content


def remove_with_inside(content, former, later, padding=''):
    pattern_a = f'{former}[^{former}{later}]+{later}'
    pattern_b = f'{former}[^{later}]+{later}'
    content = re.sub(pattern_a, padding, content)
    content = re.sub(pattern_b, padding, content)
    return content

def get_sentences(content):
    return re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', content)