import nltk
import nltk.data
import os
import json
from multiprocessing.dummy import Pool as ThreadPool
import traceback
import argparse
import re
from rake_nltk import Rake
from summa import keywords
from nltk.stem import SnowballStemmer
from keyword_extraction import keyword_extract

parser = argparse.ArgumentParser(description="Data cleaning")
parser.add_argument('--srcpath', '-s', default=r'F:\json_v2', help='Json file path, must be secondary directory')
parser.add_argument('--mode', '-m', choices=['split', 'keywords'], help='Json file path, must be secondary directory')


def get_stop_words(path):
    # print('Getting stop words ...')
    stop_words = []
    for filename in os.listdir(path):
        if filename.endswith('.txt'):
            try:
                with open(path + os.sep + filename, encoding='utf-8') as f:
                    s = f.read()
                    stop_words += [sw.lower() for sw in s.split() if sw]
            except:
                print('skipping %s' % filename)
    # num_words = len(stop_words)
    # print('Number of stop words: %i' % num_words)
    return set(stop_words)

stopwords =get_stop_words('stopwords')

def auto_split(full_path, index, length, dir):
    def remove_words(paragraphs):
        result = []
        for i in range(len(paragraphs)):
            paragraph = paragraphs[i].replace('\n', ' ')
            paragraph = paragraph.replace('\\', '')
            if len(paragraph) < 5:
                continue
            else:
                result.append(paragraph)
        return result

    try:
        print('%d / %d\t%s' % (index, length, dir))
        paper = json.load(open(full_path))['paper']
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        abstract = re.sub('%.*\n', '\n', paper['abstract'] + '\n')
        abstract = tokenizer.tokenize(abstract)
        paper['abstract'] = remove_words(abstract)

        for subtitle, section in paper['sections'].items():
            paragraphs = re.sub('%.*\n', '\n', section + '\n')
            paragraphs = paragraphs.split('\n\n')
            paper['sections'][subtitle] = remove_words(paragraphs)
        json.dump({'paper': paper}, open(full_path, 'w'))

    except Exception as e:
        print(e)
        traceback.print_exc()


def extract_keywords(full_path, index, length, dir):
    try:
        print('%d / %d\t%s' % (index, length, dir))
        paper = json.load(open(full_path))['paper']

        text_sentence = paper['abstract']
        for subtitle, section in paper['sections'].items():
            if 'introduction' in subtitle.lower() or 'background' in subtitle.lower() or 'related' in subtitle.lower():
                text_sentence.extend(section)
        key_words = keyword_extract(text_sentence,stopwords)
        
        # Rake phrases extraction
        # r = Rake(stopwords=stopwords)
        # r.extract_keywords_from_sentences(text_sentence)
        # keywords = r.get_ranked_phrases()
        #
        # text = ' '.join(paper['abstract'])
        # for subtitle, section in paper['sections'].items():
        #     if 'introduction' in subtitle.lower() or 'background' in subtitle.lower() or 'related' in subtitle.lower():
        #         text = text + ' '.join(section)

        # textRank keyword extraction
        # words = keywords.keywords(text=text, ratio=0.2, additional_stopwords=stopwords).split('\n')
        # key_words = []
        # for word in words:
        #     snowball_stemmer = SnowballStemmer('english')
        #     stem = snowball_stemmer.stem(word)
        #     if stem not in key_words:
        #         key_words.append(stem)
        #     if len(key_words) > 10:
        #         break
        # print(key_words)



    except Exception as e:
        print(e)
        traceback.print_exc()


def main(args):
    dirs = os.listdir(args.srcpath)
    if args.mode == 'split':
        for dir in dirs:
            print('%s...' % dir)
            files = os.listdir(os.path.join(args.srcpath, dir))
            pool = ThreadPool(processes=6)
            length = len(files)
            for i in range(length):
                full_path = os.path.join(args.srcpath, dir, files[i])
                # data_cleaning(full_path, i + 1, length,dir)
                pool.apply_async(auto_split, (full_path, i + 1, length, dir))
            pool.close()
            pool.join()
    elif args.mode == 'keywords':
        for dir in dirs:
            files = os.listdir(os.path.join(args.srcpath, dir))
            # pool = ThreadPool(processes=1)
            length = len(files)
            for i in range(length):
                full_path = os.path.join(args.srcpath, dir, files[i])
                extract_keywords(full_path, i + 1, length, dir)
            #     pool.apply_async(extract_keywords, (full_path, i + 1, length, dir))
            # pool.close()
            # pool.join()


if __name__ == '__main__':
    main(parser.parse_args())
