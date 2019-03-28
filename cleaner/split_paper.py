import os
import re
import json
from multiprocessing.dummy import Pool as ThreadPool
import traceback
import sys

if 'win' in sys.platform:
    path = r'F:\Dataset\json_v2'
    save_path = r'F:\Dataset\paragraph'
else:
    path = '/home/yhj/ijcai/tfidf/retriever/data/json_v1'
    save_path = '/home/yhj/ijcai/tfidf/retriever/data/paragraph'


def split_paper(dir, file, index, length):
    full_path = os.path.join(path, dir, file)
    print('%d / %d\t%s' % (index, length, dir))
    try:
        paper = json.load(open(full_path))['paper']
        abstract_id = file[:-5] + '_' + 'abstract' + '_' + '0'+'.json'
        save_name = os.path.join(save_path, dir, abstract_id)
        if paper['abstract'] != '':
            abstract = {'id': abstract_id, 'text': ' '.join(paper['abstract'])}
            json.dump(abstract,open(save_name,'w'))

        for subtitle, section in paper['sections'].items():
            for i in range(len(section)):
                if section!=[]:
                    name = re.sub('[\/:*?"<>|{}()$@%!&^]', ' ', subtitle)
                    name = '_'.join(name.split())
                    section_id = file[:-5] + '_' + name + '_' + str(i)+'.json'
                    save_name = os.path.join(save_path, dir, section_id)
                    json.dump({'id':section_id,'text':paper['sections'][subtitle][i]},open(save_name,'w'))

    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == '__main__':
    dirs = os.listdir(path)
    for dir in dirs:
        files = os.listdir(path + '/' + dir)
        print(dir + '...')
        pool = ThreadPool(processes=6)
        if not os.path.exists(save_path + '/' + dir):
            os.makedirs(save_path + '/' + dir)
        length = len(files)
        for i in range(0, length):
            # split_paper(dir, files[i], i + 1, length)
            pool.apply_async(split_paper, (dir, files[i], i + 1, length))
        pool.close()
        pool.join()
