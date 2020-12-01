import re
import unicodedata

KOREAN_SYLLABABLES = re.compile('[\uAC00-\uD7AF]', re.UNICODE)
KOREAN_JAMO = re.compile('[\u1100-\u11FF]', re.UNICODE)
KOREAN_JAMO_COMPAT = re.compile('[\uAC00-\uD7AF]', re.UNICODE)
KOREAN_JAMO_EXTEND_A = re.compile('[\uA960-\uA97F]', re.UNICODE)
KOREAN_JAMO_EXTEND_B = re.compile('[\uD7B0-\uD7FF]', re.UNICODE)

ENG = re.compile('[가-힣]')

if __name__=='__main__':
    pass