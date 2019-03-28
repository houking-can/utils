import re
import os
import json
from multiprocessing.dummy import Pool as ThreadPool
import traceback
from tex2py import tex2py
import shutil
import TexSoup

tex_path = r'F:\Dataset\arxiv_tex'
json_save_path = r'F:\Dataset\arxiv_json'
json_discard_path = r'F:\Dataset\arxiv_json_discard'
bbl_path = r'F:\Dataset\arxiv_full'
tex_error_path = r'F:\Dataset\arxiv_tex_error'
tex_discard_path = r'F:\Dataset\arxiv_tex_discard'
complete_tex_path = r'F:\Dataset\complete_arxiv_tex'

def extract(dir, file, index):
    full_tex_path = os.path.join(tex_path, dir, file)
    tex = open(full_tex_path, 'r', errors='ignore').read()
    paper = {"category": dir, "id": file[:-4]}
    try:
        tex_tree = tex2py(tex)
        # title, author , abstract and section
        title = ''
        author = ''
        abstract = ''
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
                            abstract+=x

                elif descendant.name == "titlepage":
                    for each in list(descendant.expr.contents):
                        if isinstance(each, TexSoup.TexNode) and each.name == "abstract":
                            for x in list(each.expr.contents):
                                if isinstance(x, TexSoup.TokenWithPosition):
                                    abstract += x
                            break

                elif descendant.name=='cite' and current_section!='':
                    try:
                        section[current_section] = section[current_section] + '{cite ' + ''.join(list(descendant.expr.contents)) + '}'
                    except:
                        print("Add cite error!")
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

        # references = re.findall('bibitem(.*?)\n(.*)', tex)
        # if len(references) == 0:
        #     full_bbl_path = os.path.join(bbl_path, dir, file[:-4])
        #     bbl_files = os.listdir(full_bbl_path)
        #     for each in bbl_files:
        #         if each.endswith('.bbl'):
        #             bbl = open(full_bbl_path+'/'+each, 'r', errors='ignore').read()
        #             references = re.findall('bibitem(.*?)\n(.*)', bbl)
        #             print('bbl reference length : ' + str(len(references)))
        #             break

        paper = dict({"title": title,
                      "author": author,
                      "abstract": ''.join(abstract),
                      "sections": section
                      },
                     **paper)

        if title == '' or author == '' or abstract == '' or section == {} :
            if not os.path.exists(json_discard_path + '/' + dir):
                os.makedirs(json_discard_path + '/' + dir)
            json.dump({'paper': paper}, open(json_discard_path + '/' + dir + '/' + file[:-4] + '.json', 'w'))
            if not os.path.exists(tex_discard_path + '/' + dir):
                os.makedirs(tex_discard_path + '/' + dir)
            shutil.move(full_tex_path, tex_discard_path + '/' + dir)
            print(str(index + 1) + '/' + str(len(files)) + '\tNot complete!'+'\t\t'+file)

        else:
            if not os.path.exists(json_save_path + '/' + dir):
                os.makedirs(json_save_path + '/' + dir)
            json.dump({'paper': paper}, open(json_save_path + '/' + dir + '/' + file[:-4] + '.json', 'w'))
            if not os.path.exists(complete_tex_path + '/' + dir):
                os.makedirs(complete_tex_path + '/' + dir)
            shutil.move(full_tex_path, complete_tex_path + '/' + dir)
            print(str(index + 1) + '/' + str(len(files)) + '\tComplete!'+'\t\t'+file)

    except Exception as e:
        if 'Malformed argument' or 'Expecting' in str(e):
            if not os.path.exists(tex_error_path + '/' + dir):
                os.makedirs(tex_error_path + '/' + dir)
            shutil.move(full_tex_path, tex_error_path + '/' + dir)
            print(str(index + 1) + '/' + str(len(files)) + '\tTex error!'+'\t\t'+file)

        else:
            print(e)
            traceback.print_exc()

if __name__ == '__main__':
    dirs = os.listdir(tex_path)
    for dir in dirs:
        files = os.listdir(tex_path + '/' + dir)
        print(dir + '...')
        papers = []
        pool = ThreadPool(processes=6)

        for i in range(0, len(files)):
            pool.apply_async(extract, (dir, files[i], i))
            # extract(dir, files[i], i)
        pool.close()
        pool.join()