import re
import string
import unicodedata

KOREAN_SYLLABABLES = u'\uAC00-\uD7AF'
KOREAN_JAMO = u'\u1100-\u11FF'
KOREAN_JAMO_COMPAT = u'\u3130-\u318F'
KOREAN_JAMO_EXTEND_A = u'\uA960-\uA97F'
KOREAN_JAMO_EXTEND_B = u'\uD7B0-\uD7FF'


def rm_char_ecpt_patterns(content, patterns=[]):
    return re.sub(f"[^{''.join(patterns)}]", '', content)


def rm_char_patterns(content, patterns=[]):
    return re.sub("{{.}}", '', content)


def rm_embedded_string(text, former, later):
    '''

    :param text: text to convert
    :param former: former string
    :param later: later string
    :return: converted texts
    '''
    text = re.sub(f'(?<={former}).+(?={later})', '', text)
    text = re.sub(f'[{former}{later}]', '', text)
    return text


if __name__ == '__main__':
    text = '안녕{{출처 필요|날짜=2015-10-16}}하세요'
    result = rm_char_patterns(text, patterns=['{{','[.]','}}'])
    print(rm_embedded_string(text, '{{', '}}'))