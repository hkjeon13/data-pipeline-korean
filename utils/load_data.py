from lxml import etree
from tqdm import tqdm


def load_koquad2(path):
    titles, contents = [], []
    t_append,c_append = titles.append, contents.append
    for _, e in tqdm(etree.iterparse(path)):
        etag = e.tag.split('}')[-1]
        if etag=='title':
            t_append(e.text)
        elif etag=='text':
            c_append(e.text)
        e.clear()
    return titles, contents


if __name__ == '__main__':
    titles, contents = load_koquad2('../data/kowiki-20200401-pages-meta-current.xml')
    print(contents[432])