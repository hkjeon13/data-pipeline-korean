import re
import time
import pandas as pd
from lxml import etree
from tqdm import tqdm
from itertools import compress

LINK = '(http|https)://[a-zA-Z0-9\./=#_%~&\-\?:]+'
SENTENCE = '(?<=[가-힣ㄱ-ㅎa-z])(\.|\?|!) ?(?=[가-힣ㄱ-ㅎA-Z])'
DELI_SEN = '?!.'


def load_kowiki(path):
    contents = []
    c_append = contents.append
    for _, e in tqdm(etree.iterparse(path)):
        etag = e.tag.split('}')[-1]
        if etag == 'text':
            c_append(preprocessing_new(e.text))
        e.clear()
    return contents


def rm_embedded_string(text, former, later):
    text = re.sub(f'(?<={former})[^{later}]+(?={later})', '', text)
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

            patterns = [['\[\[.+\]\](?![ 가-힣a-zA-Z,\.])', ''], [' {2,}', ' '], ['\n{3,}', '\n\n'],
                        ['(?<=\[\[)[^\]]+\|(?=[^\]]+\]\])', ''], ['[\[\]]{2}', ''],
                        ['(?<=\n)(\*? ?:+ ?|\*[ :]?|#)', ''], ['={2,}', ''], [LINK,''],
                        ['\"{2}', "\'"], ['[\'\"]{2,}', ''] ,['\-\-[^\n]+', ''], ['\(,? ?\)', ''], ['\|.+(?=\n)', '']]
            for pattern, repl in patterns:
                content = re.sub(pattern, repl, content)
        sentences = get_sentences(content)

        contents = []
        append = contents.append
        hangul = re.compile('.+(다|요|까)(\.|\?|!)')
        for sentence in sentences:
            splited = [re.sub('^[\*!: \-\)#]', '', s) for s in sentence.split('\n') if hangul.match(s)]
            append('\n'.join(splited))
        return contents


def preprocessing_new(content, mode='korquad2-sens-kor'):
    if not isinstance(content, str):
        return content
    if mode == 'korquad2-sens-kor':
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
        content = re.sub('(파일:[^\|\n]+[\|\n])|(섬네일\|)', '', content)
        content = re.sub('\[\]','', content)
        content = re.sub('(?<=\n)[\'/ ]+', '', content)
        content = re.sub('\(, \)', '', content)
        content = '\n'.join(list(filter(
            lambda x: len(x.split()) > 3 and re.compile('[가-힣]').match(x),
            get_sentences(content))))
        content = re.sub('(?<=\n)[^가-힣]+(?=\n)', '', content)
        content = re.sub('(?<=\n)\[.+\](?=\n)', '', content)
        content = re.sub('(?<=[ 가-힣])[\[\]](?=[ 가-힣])','',content)
        content = re.sub('\n{2,}','\n\n', content)

    return content


def remove_with_inside(content, former, later):
    pattern_a = f'{former}[^{former}{later}]+{later}'
    pattern_b = f'{former}[^{later}]+{later}'
    content = re.sub(pattern_a, '', content)
    content = re.sub(pattern_b, '', content)
    return content

def if_matching_hangul(match):
    return None if match.group('not_hangul') else None


def get_sentences(content):
    return re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', content)


def save_sentences(path, contents):
    with open(path, 'w', encoding='utf-8') as w:
        w.write(contents)


if __name__ == '__main__':
    contents = load_kowiki('../data/kowiki-20200401-pages-meta-current.xml')
    contents = '\n\n'.join(list(compress(contents, contents)))
    save_sentences('../outputs/refined.txt', contents)