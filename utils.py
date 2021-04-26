def load_text(path):
    with open(path, 'r', encoding='utf-8') as r:
        content = r.read()
    return content

def write_text(path, content):
    with open(path, 'w', encoding='utf-8') as w:
        w.write(content)

if __name__ =='__main__':
    path = './file_extension.txt'
    write_text(path, load_text(path).lower())