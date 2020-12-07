import re
import json
from lxml import etree
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial

LINK = '(http|https)://[가-힣a-zA-Z0-9\./=#_%~&\-\?:;\(\)]+'
SENTENCE = '(?<=[가-힣ㄱ-ㅎa-z])(\.|\?|!) ?(?=[가-힣ㄱ-ㅎA-Z])'
DELI_SEN = '?!.'


def kowiki_sentences(path, mode='kowiki-sens-kor'):
    contents = []
    c_append = contents.append
    for _, e in tqdm(etree.iterparse(path)):
        etag = e.tag.split('}')[-1]
        if etag == 'text':
            c_append(preprocessing(e.text, mode=mode))
        e.clear()
    return contents


def korquad2_sentences(path, num_cores, mode='korquad2-sens-kor'):
    contents = load_json(path)
    contents = list(map(lambda x: x['context'], contents['data']))
    func = partial(preprocessing, mode=mode)
    outputs = run_imap_multiprocessing(func, contents, num_cores)
    return outputs


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
        content = remove_with_inside(content, '<', '>')
        content = remove_with_inside(content, '{{', '}}')
        content = remove_with_inside(content, '{', '}')
        content = re.sub('{}', '', content)
        content = re.sub('(?<=\n)[ :;#\*\-]+', '', content)
        content = re.sub('(?<=\[\[)[^\[]+\|(?=[^\|\]]+\]\])', '', content)
        content = re.sub('[\[\]]{2,}', '', content)
        content = re.sub("\'{2,}", '\'', content)
        content = re.sub("\"{2,}", '\"', content)
        content = re.sub("={2,}", '', content)
        content = re.sub(LINK, '', content)
        content = re.sub('\[\]','', content)
        content = re.sub('(?<=\n)\'+', '', content)
        content = re.sub('(?<=\n)/+', '', content)
        content = re.sub('(?<=\n) +', '', content)
        content = re.sub('\(, \)', '', content)
        content = '\n'.join(list(filter(
            lambda x: len(x.split()) > 3 and re.compile('[가-힣]').match(x),
            get_sentences(content))))
        content = re.sub('(?<=\n)[^가-힣]+(?=\n)', '', content)
        content = re.sub('(?<=\n)\[.+\](?=\n)', '', content)
        content = re.sub('(?<=[ 가-힣])[\[\]](?=[ 가-힣])','',content)
        content = re.sub('\n{2,}','\n\n', content)

    elif mode == 'korquad2-sens-kor':
        content = remove_with_inside(content, '<', '>', padding='')
        content = re.sub(LINK, '', content)
        content = re.sub('\[편집\]', '', content)
        content = re.sub('(?<=\n)[↑\-]', '', content)
        content = re.sub('(?<=\n)분류:.+(?=\n)', '', content)
        content = re.sub('(?<=[ 가-힣])[\[\]](?=[ 가-힣])', '', content)
        sentences = []
        for c in content.split('\n'):
            if (len(c.split()) > 3 and re.compile('[가-힣]').match(c)) or (c==''):
                sentences.append(c)
        content = '\n'.join(sentences)
        content = get_sentences(content)
        content = '\n'.join(content)
        content = re.sub('(?<=[ 가-힣])[\[\]](?=\n)', '', content)
        content = re.sub('\n{2,}', '\n\n', content)
        content = re.sub('\[[0-9]+\](?=\n)', '', content)
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