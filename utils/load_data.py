import pandas as pd
from lxml import etree
from tqdm import tqdm
import re
import time
import gc
from multiprocessing import Pool, cpu_count
from functools import partial
from itertools import compress

LINK = 'http[s]?://[a-zA-Z0-9\./=#_\-\?\\]+'
SENTENCE = '(?<=[가-힣ㄱ-ㅎa-z])(\.|\?|!) ?(?=[가-힣ㄱ-ㅎA-Z])'
DELI_SEN = '?!.'

KOREAN_SYLLABABLES = u'\uAC00-\uD7AF'
KOREAN_JAMO = u'\u1100-\u11FF'
KOREAN_JAMO_COMPAT = u'\u3130-\u318F'
KOREAN_JAMO_EXTEND_A = u'\uA960-\uA97F'
KOREAN_JAMO_EXTEND_B = u'\uD7B0-\uD7FF'


def run_imap_multi_2(func, argument_list, num_processes):
    pool = Pool(processes=num_processes)
    result_list_tqdm = []
    for result in tqdm(pool.imap(func=func, iterable=argument_list), total=len(argument_list)):
        result_list_tqdm.append(result)
    return result_list_tqdm


def load_koquad2(path):
    titles, contents = [], []
    t_append, c_append = titles.append, contents.append
    for _, e in tqdm(etree.iterparse(path)):
        etag = e.tag.split('}')[-1]
        if etag == 'title':
            t_append(e.text)
        elif etag == 'text':
            c_append(preprocessing(e.text))
        e.clear()
    return titles, contents


def get_kor_sentences(content):
    sentences = re.split(SENTENCE, content)
    new_sentences, deli = [''], list(DELI_SEN)
    append = new_sentences.append
    for s in sentences:
        if s in deli:
            new_sentences[-1] += s
        else:
            if re.match('[가-힣]', s):
                append(s)
    return new_sentences


def preprocessing(content, mode='korquad2-sens-kor'):
    if isinstance(content, str):
        if mode == 'korquad2-sens-kor':
            content = content.strip()

            char_pairs= [['<', '>'], ['{{', '}}'], ['\[\[', '\]\]'], ['==', '==']]
            patterns = [f'({former}[^{later}]'+'{'+str(len(later))+',}'+f'{later})' for former, later in char_pairs]
            pattern = '|'.join(patterns)
            content = re.sub(pattern, '', content)
#            replace_pair = [['(?<!\")\"\"(?!\")', "\'"]]
#            for k, v in replace_pair:
#                content = re.sub(k, v, content)

#            pattern = [LINK, '\|+.+\n', '\=', '\* [:]?', '\([\, ]?\)', '\|', '\*+[ ]?']
#            pattern = '|'.join(pattern)
#            content = re.sub(pattern, '', content)
#            content = re.sub("(\'|\"|\-){2,}",'', content)
#            content = re.sub('(?<![가-힣])(\(.\))?[\.\?!]+', '', content)
    return content


if __name__ == '__main__':
    print('returned memory:', gc.collect())
    titles, contents = load_koquad2('../data/kowiki-20200401-pages-meta-current.xml')
    df_data = pd.DataFrame({'title': titles, 'content': contents})
    df_data.to_csv('../outputs/korquad2_refine_8.csv', encoding='utf-8', index=False)

    #text = '<body>안녕하세요. ==만나서==반갑습니다.</body>'
    #result = re.sub('(<[^>]+>)|(==[^==]+==)', '', text)
    #print(result)