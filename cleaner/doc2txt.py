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
		# ��Ŀ¼�������ļ�������
		files = os.listdir(path)
		# ��Ŀ�´���һ����Ŀ¼newdir��������ת�����txt�ı�
		# New_dir = os.path.abspath(os.path.join(path, 'newdir'))
		# if not os.path.exists(New_dir):
			# os.mkdir(New_dir)

		# ����һ���ı��������е�word�ļ���
		# fileNameSet = os.path.abspath(os.path.join(New_dir, 'fileNames.txt'))
		# o = open(fileNameSet, "w")

		for filename in files:

			# �������word�ļ�������
			if not fnmatch.fnmatch(filename, '*.doc') and not fnmatch.fnmatch(filename, '*.docx') and not  fnmatch.fnmatch(filename, '*.rtf'):
				continue;
			# �����word��ʱ�ļ�������
			if fnmatch.fnmatch(filename, '~$*'):
				continue;

			docpath = os.path.abspath(os.path.join(path, filename))

			# �õ�һ���µ��ļ���,��ԭ�ļ����ĺ�׺�ĳ�txt
			new_txt_name = ''
			if fnmatch.fnmatch(filename, '*.doc') or fnmatch.fnmatch(filename, '*.rtf'):
				new_txt_name = filename[:-4] + '.txt'
			else:
				new_txt_name = filename[:-5] + '.txt'

			word_to_txt = os.path.join(os.path.join(path), new_txt_name)
			print word_to_txt
			wordapp = wc.Dispatch('Word.Application')
			doc = wordapp.Documents.Open(docpath)
			# Ϊ����python�����ں���������r��ʽ��ȡtxt�Ͳ��������룬����Ϊ4
			doc.SaveAs(word_to_txt, 4)
			doc.Close()
			# o.write(word_to_txt + '\n')





