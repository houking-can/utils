import os
import sys
import shutil

path = r'F:\Dataset\arxiv_processed'
save_base = r'F:\Dataset\arxiv_tex'

if not os.path.exists(save_base):
    os.makedirs(save_base)

dirs = os.listdir(path)

for dir in dirs:
    print(dir + '...\n')
    save_path = save_base + '/' + dir
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    files = os.listdir(path + '/' + dir)
    for file in files:
        full_path = path + '/' + dir + '/' + file

        if os.path.isdir(full_path):
            sub_files = os.listdir(full_path)

            for each in sub_files:
                if each.lower().endswith('.tex') and os.path.getsize(full_path + '/' + each) > 20240:
                    shutil.copy(full_path + '/' + each, save_path + '/' + file+'.tex')
                    break

        elif file.lower().endswith('.tex'):
            shutil.move(full_path, save_path)
