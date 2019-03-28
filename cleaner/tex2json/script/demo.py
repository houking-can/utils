import re
import os
import json
import time
from multiprocessing.dummy import Pool as ThreadPool
from tex2py import tex2py
import shutil
import TexSoup

tex_path = r'C:\Users\Houking\Desktop\arxiv'
json_save_path = r'C:\Users\Houking\Desktop\arxiv_json'
json_discard_path = r'C:\Users\Houking\Desktop\arxiv_discard_json'
bbl_path = r'F:\Dataset\arxiv_full'
tex_error_path = r'C:\Users\Houking\Desktop\error'
tex_discard_path = r'C:\Users\Houking\Desktop\discard'


def extract(dir, file, index):
    full_tex_path = os.path.join(tex_path, dir, file)
    tex = open(full_tex_path, 'r', errors='ignore').read()
    paper = {"category": dir, "id": file[:-4]}
    try:
        tex_tree = tex2py(tex)
        # title, author , abstract and section
        title = ''
        author = ''
        abstract = []
        section = {}
        current_section = ''
        level_1 = 0
        level_2 = 0
        level_3 = 0
        for descendant in tex_tree.descendants:
            if isinstance(descendant, TexSoup.TexNode):
                if descendant.name == "title":
                    title = descendant.string
                elif descendant.name == "author":
                    author = descendant.string
                elif descendant.name == "abstract":
                    for x in list(descendant.expr.contents):
                        if isinstance(x, TexSoup.TokenWithPosition):
                            abstract.append(x)

                elif descendant.name == "titlepage":
                    for each in list(descendant.expr.contents):
                        if each.name == "abstract":
                            for x in list(each.expr.contents):
                                if isinstance(x, TexSoup.TokenWithPosition):
                                    abstract.append(x)
                            break

                elif 'cite' in descendant.name:
                    section[current_section] = section[current_section] + '{cite ' + descendant.string + '}'
                elif 'section' in descendant.name:
                    if 'subsub' in descendant.name:
                        level_3 += 1
                        current_section = str(level_1) + '.' + str(level_2) + '.' + str(
                            level_3) + ' ' + descendant.string
                    elif 'sub' in descendant.name:
                        level_2 += 1
                        current_section = str(level_1) + '.' + str(level_2) + ' ' + descendant.string
                    else:
                        level_1 += 1
                        level_2 = 0
                        level_3 = 0
                        current_section = str(level_1) + '.' + descendant.string
                    section[current_section] = ''
                elif "bibitem" in descendant.name:
                    break
            elif isinstance(descendant, TexSoup.TokenWithPosition) and current_section != '':
                section[current_section] = section[current_section] + ' ' + descendant
            else:
                continue

        references = re.findall('bibitem(.*?)\n(.*)', tex)
        if len(references) == 0:
            full_bbl_path = os.path.join(bbl_path, dir, file)
            bbl_files = os.listdir(full_bbl_path)
            for each in bbl_files:
                if each.endswith('.bbl'):
                    bbl = open(full_bbl_path, 'r', errors='ignore').read()
                    references = re.findall('bibitem(.*?)\n(.*)', bbl)
                    break

        # if len(references) > 0:
        #     print(str(index + 1) + '.json' + ' ' + file + ' ' + str(len(references)))
        paper = dict({"title": title,
                      "author": author,
                      "abstract": ''.join(abstract),
                      "sections": section,
                      "references": references},
                     **paper)

        if title == '' or author == '' or abstract == '' or section == {} or references==[]:
            if not os.path.exists(json_discard_path + '/' + dir):
                os.makedirs(json_discard_path + '/' + dir)
            json.dump({'papers': paper}, open(json_discard_path + '/' + dir + '/' + str(index + 1) + '.json', 'w'))
            if not os.path.exists(tex_discard_path + '/' + dir):
                os.makedirs(tex_discard_path + '/' + dir)
            shutil.move(full_tex_path, tex_discard_path + '/' + dir)
            print(str(index + 1) + '/' + str(len(files)) + '   Not complete!')

        else:
            if not os.path.exists(json_save_path + '/' + dir):
                os.makedirs(json_save_path + '/' + dir)
            json.dump({'papers': paper}, open(json_save_path + '/' + dir + '/' + str(index + 1) + '.json', 'w'))
            print(str(index + 1) + '/' + str(len(files)) + '   Complete!')

    except Exception as e:
        if 'Malformed argument' in str(e):
            if not os.path.exists(tex_error_path + '/' + dir):
                os.makedirs(tex_error_path + '/' + dir)
            shutil.move(full_tex_path, tex_error_path + '/' + dir)


if __name__ == '__main__':
    dirs = os.listdir(tex_path)
    for dir in dirs:
        files = os.listdir(tex_path + '/' + dir)
        print(dir + '...')
        papers = []
        pool = ThreadPool(processes=6)
 
        for i in range(0,len(files)):
            pool.apply_async(extract, (dir, files[i], i))
            # extract(dir, files[i], i)
        pool.close()
        pool.join()