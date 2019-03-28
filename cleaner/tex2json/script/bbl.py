import re
import os
from multiprocessing.dummy import Pool as ThreadPool
import json
import traceback
import shutil

tex_path = r'F:\Dataset\arxiv_tex'
json_save_path = r'F:\Dataset\arxiv_json'
json_discard_path = r'F:\Dataset\arxiv_json_discard'
bbl_path = r'F:\Dataset\arxiv_full'
tex_error_path = r'F:\Dataset\arxiv_tex_error'
tex_discard_path = r'F:\Dataset\arxiv_tex_discard'
complete_tex_path = r'F:\Dataset\complete_arxiv_tex'


def get_bbl(dir, file, index):
    try:
        data = json.load(open(os.path.join(json_save_path, dir, file)))
        full_tex_path = os.path.join(complete_tex_path, dir, file[:-5] + '.tex')

        tex = []
        temp = open(full_tex_path, 'r', errors='ignore').readlines()
        for each in temp:
            if '%' not in each:
                tex.append(each)
        tex = ''.join(tex)

        tex = tex.replace(r'\bibitem', '#' + r'\bibitem')
        tex = tex.replace(r'\end', '#' + r'\end')
        references = []
        flag = 0
        if r'\bibitem' in tex:
            flag = 1
            references = re.findall(
                '\\\\bibitem\{(.*?)\}((?:.|[\r\n])*?)\\\\newblock((?:.|[\r\n])*?)\\\\newblock((?:.|[\r\n])*?)#', tex)
            if (len(references) == 0):
                references = re.findall('\\\\bibitem((?:.|[\r\n])*?)#', tex)

        else:
            full_bbl_path = os.path.join(bbl_path, dir, file[:-5])
            bbl_files = os.listdir(full_bbl_path)

            for each in bbl_files:

                if each.endswith('.bbl'):
                    flag = 1

                    bbl = []
                    temp = open(full_bbl_path + '/' + each, 'r', errors='ignore').readlines()
                    for each in temp:
                        if '%' not in each:
                            bbl.append(each)
                    bbl = ''.join(bbl)
                    bbl = bbl.replace(r'\bibitem', '#' + r'\bibitem')
                    bbl = bbl.replace(r'\end', '#' + r'\end')

                    references = re.findall(
                        '\\\\bibitem\{(.*?)\}((?:.|[\r\n])*?)\\\\newblock((?:.|[\r\n])*?)\\\\newblock((?:.|[\r\n])*?)#',
                        bbl)
                    if (len(references) == 0):
                        references = re.findall('\\\\bibitem((?:.|[\r\n])*?)#', bbl)

                    break
        if (len(references) == 0):
            if flag:
                print(dir + ':' + file[:-5] + '\tdiscard')
            else:
                print(dir + ':' + file[:-5] + '\textract failed!')
            shutil.move(full_tex_path, tex_discard_path + '/' + dir)
            shutil.move(os.path.join(json_save_path, dir, file), json_discard_path + '/' + dir)
        else:
            data['paper']['references'] = references
            json.dump(data,open(os.path.join(json_save_path, dir, file),'w'))
            print(str(index + 1) + '/' + str(len(files)) + '\tComplete!' + '\t' + file)

    except Exception as e:
        print(e)
        traceback.print_exc()
        print(str(index + 1) + '/' + str(len(files)) + '\tError!' + '\t' + file)


if __name__ == '__main__':
    dirs = os.listdir(json_save_path)
    for dir in dirs:
        files = os.listdir(json_save_path + '/' + dir)
        print(dir + '...')
        pool = ThreadPool(processes=6)

        for i in range(0, len(files)):
            pool.apply_async(get_bbl, (dir, files[i], i))
            # get_bbl(dir, files[i], i)
        pool.close()
        pool.join()
