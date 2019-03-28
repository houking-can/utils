import os

path = '/mnt/hgfs/a/test'
save_base = '/mnt/hgfs/a/des'

dirs = os.listdir(path)
for dir in dirs:
    category = dir
    files = os.listdir(path+'/'+dir)
    print(dir+'...')
    for file in files:
        full_path = path + '/' + dir + '/' + file
        save_path = save_base + '/' + dir + '/' + file
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        os.system('latex2html ' + full_path + ' -dir ' + save_path)
