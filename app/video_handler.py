import os


def find_lists(basedir='.'):
    res = []
    for b, dirs, files in os.walk(basedir):
        flag = False
        for f in files:
            if f.endswith('avi'):
                flag = True
        if flag:
            res.append(b)
    return res


def list_files(listname):
    res = [f for f in os.listdir(listname) if f.endswith('avi')]
    return res


def get_file_contents(file):
    with open(file, 'rb') as f:
        return f.read()


if __name__ == '__main__':
    lists = find_lists('/home/borsuk/video')
    print(lists)
    for l in lists:
        print(list_files(l))

