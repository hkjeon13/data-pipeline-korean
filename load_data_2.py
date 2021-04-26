import re


def split_sentences(corpus):
    return re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', corpus)


class TextPreprocess(object):
    def __init__(self):
        self.process = {
            'LINK' : '(http|https)://[가-힣a-zA-Z0-9\./=#_%~&\-\?:;\(\)]+',
            'FILE' : '[가-힣0-9a-zA-Z_\-]\.(jpg|jpeg|png|svg|txt|gif)',
        }

    def call(self):
        pass


if __name__=='__main__':
    result = split_sentences('안녕하세요? 만나서 반갑습니다.')
    print(result)