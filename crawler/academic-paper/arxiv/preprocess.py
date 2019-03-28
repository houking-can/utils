import os
import tarfile
import shutil
from PyPDF2 import PdfFileReader

def isValidPDF(filename):
    bValid = True
    try:
        read = PdfFileReader(filename)
    except:
        bValid = False
    return bValid


des_path = r'F:\result'
sou_path = r'F:\source'

dirs  = os.listdir(sou_path)
for dir in dirs:
    files = os.listdir(sou_path+'/'+dir)
    length = len(files)
    cnt = 1
    for file in files:
        print( dir + ' : '+ str(cnt)+'/'+str(length))
        cnt+=1
        d_path = des_path+ '/' + dir + '/tar/'+file +'/'
        s_path = sou_path +'/' + dir +'/'+file
        file_size = os.path.getsize(s_path)
        if file_size < 2000:
            os.remove(s_path)
            continue
        try:
            tar = tarfile.open(s_path)
            names = tar.getnames()
            if not os.path.isdir(d_path):
                os.makedirs(d_path)
            try:
                tar.extractall(d_path)
                tar.close()
                shutil.move(s_path, des_path + '/' + dir + '/' + file + '.tar')
                if os.path.isfile(s_path):
                    os.remove(s_path)
            except:
                continue
            # for name in names:
            #     tar.extract(name, d_path)

        except:
            if isValidPDF(s_path):
                shutil.move(s_path, des_path + '/' + dir + '/' + file.replace('.pdf', '') + '.pdf')
                if os.path.isfile(s_path):
                    os.remove(s_path)
                continue
            else:
                text = open(s_path, 'rb').read()
                if b'\documentstyle' in text or b'\documentclass' in text or b'\end{document}' in text:
                    shutil.move(s_path, des_path + '/' + dir + '/' + file + '.tex')
                    if os.path.isfile(s_path):
                        os.remove(s_path)
                elif b'<!DOCTYPE' in text:
                    shutil.move(s_path, des_path + '/' + dir + '/' + file + '.html')
                    if os.path.isfile(s_path):
                        os.remove(s_path)
                else:
                    shutil.move(s_path, des_path + '/' + dir + '/' + file + '.tex')
                    if os.path.isfile(s_path):
                        os.remove(s_path)