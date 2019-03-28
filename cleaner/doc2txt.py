# -*- coding: cp936 -*-

from win32com import client as wc
import os
import fnmatch
import sys

all_FileNum = 0


if __name__ == '__main__':

	dir = os.listdir(sys.argv[1])
	for each_dir in dir:
		rootPATH=sys.argv[1]
		# print rootPATH
		# print(each_dir)
		path = rootPATH + '\\' + each_dir + '\\' 
		print each_dir
		# 该目录下所有文件的名字
		files = os.listdir(path)
		# 该目下创建一个新目录newdir，用来放转化后的txt文本
		# New_dir = os.path.abspath(os.path.join(path, 'newdir'))
		# if not os.path.exists(New_dir):
			# os.mkdir(New_dir)

		# 创建一个文本存入所有的word文件名
		# fileNameSet = os.path.abspath(os.path.join(New_dir, 'fileNames.txt'))
		# o = open(fileNameSet, "w")

		for filename in files:

			# 如果不是word文件：继续
			if not fnmatch.fnmatch(filename, '*.doc') and not fnmatch.fnmatch(filename, '*.docx') and not  fnmatch.fnmatch(filename, '*.rtf'):
				continue;
			# 如果是word临时文件：继续
			if fnmatch.fnmatch(filename, '~$*'):
				continue;

			docpath = os.path.abspath(os.path.join(path, filename))

			# 得到一个新的文件名,把原文件名的后缀改成txt
			new_txt_name = ''
			if fnmatch.fnmatch(filename, '*.doc') or fnmatch.fnmatch(filename, '*.rtf'):
				new_txt_name = filename[:-4] + '.txt'
			else:
				new_txt_name = filename[:-5] + '.txt'

			word_to_txt = os.path.join(os.path.join(path), new_txt_name)
			print word_to_txt
			wordapp = wc.Dispatch('Word.Application')
			doc = wordapp.Documents.Open(docpath)
			# 为了让python可以在后续操作中r方式读取txt和不产生乱码，参数为4
			doc.SaveAs(word_to_txt, 4)
			doc.Close()
			# o.write(word_to_txt + '\n')





