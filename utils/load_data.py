import re
import time
import pandas as pd
from lxml import etree
from tqdm import tqdm
from itertools import compress

LINK = '(http|https)://[a-zA-Z0-9\./=#_%~\-\?:]+'
SENTENCE = '(?<=[가-힣ㄱ-ㅎa-z])(\.|\?|!) ?(?=[가-힣ㄱ-ㅎA-Z])'
DELI_SEN = '?!.'


def load_koquad2(path):
    titles, contents = [], []
    t_append, c_append = titles.append, contents.append
    for _, e in tqdm(etree.iterparse(path)):
        etag = e.tag.split('}')[-1]
        if etag == 'title':
            t_append(e.text)
        elif etag == 'text':
            c_append(preprocessing(e.text))
#            c_append(e.text)
        e.clear()
    return titles, contents


def rm_embedded_string(text, former, later):
    text = re.sub(f'(?<={former}).+(?={later})', '', text)
    text = re.sub(f'[{former}{later}]', '', text)
    return text


def preprocessing(content, mode='korquad2-sens-kor'):
    if isinstance(content, str):
        if mode == 'korquad2-sens-kor':
            content = content.strip()
            content = re.sub('(?<=\[\[)(?<=[a-zA-Z0-9가-힣])\|[a-zA-Z0-9가-힣 ]+(?=\]\])]','', content)
            content = re.sub('(?<=\n)\|.+(?=\n)', '', content)
            char_pairs = [['<', '>'], ['{{', '}}']]
            for former, later in char_pairs:
                content = rm_embedded_string(content, former, later)

            patterns = [LINK, '\n:+ ?', '\* [:]?', '[\[\]=]{2,}',':{.+(?=\n)'
                        '\([\, ]?\)', "[\'\"\-]{2,}", "(?<=\n):", '파일:.+(?<=\|)', '\|.+(?<!\n)', '[^\.]+\n']

            for pattern in patterns:
                content = re.sub(pattern, '', content)

    return content

'''
            replace_pair = [['(?<!\")\"\"(?!\")', "\'"]]
            for k, v in replace_pair:
                content = re.sub(k, v, content)
            #'[\[\]=]{2,}'
            patterns = [LINK, '\n:+ ?', '(?<=\n)\|+.+(?=\n)', '\|[a-zA-Z]+ ?' 
                        '\* [:]?', '\([\, ]?\)', "[\'\"\-]{2,}", "(?<=\n):"]
            for pattern in patterns:
                content = re.sub(pattern, '', content)
            m = re.compile('(?P<not_hangul>((?<=[가-힣](\.|\?|!))[^가-힣]+[\.\?!]))')
            content = m.sub(if_matching_hangul, content)
            content = re.sub('\n{2,}', '\n', content)
            content = re.sub('\t{2,}', '\t', content)
            content = get_sentences(content)
            content = list(filter(lambda c: len(c) > 10, content))
            content = [re.sub('^[^가-힣]', '', c.strip()) for c in content]
'''


def if_matching_hangul(match):
    return None if match.group('not_hangul') else None


def get_sentences(content):
    return re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', content)


if __name__ == '__main__':
    titles, contents = load_koquad2('../data/kowiki-20200401-pages-meta-current.xml')
    df_data = pd.DataFrame({'title': titles, 'content': contents})
    df_data.to_csv('../outputs/korquad2_refine_3.csv', encoding='utf-8', index=False)
