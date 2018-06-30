# -*- coding: utf-8 -*-
from nltk.tokenize import WordPunctTokenizer
import pickle
import csv
import collections

""" database format: index article_index vol book  title author content num_words """
database_file = open("/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_whole_database.csv",'r')
database = csv.reader(database_file)
word_tag_dict = collections.defaultdict(str)
count = 0
gtoken = WordPunctTokenizer()
punctuations = ['+','{','}','...','*','&','-','(',')','<','>','[',']','\'','\"',':',',','.','?','!']
with open('nltk_german_classifier.pickle', 'rb') as f:
    tagger = pickle.load(f)
for line in database:
    if count!= 0:
        print count
        original_text = line[-2].strip()
        tokenize_text = gtoken.tokenize(original_text.decode('utf-8'))
        clean_tokenize_text = [item for item in tokenize_text if not item in punctuations]
        tagged = tagger.tag(clean_tokenize_text)
        for item in tagged:
            word_tag_dict[item[0]] = item[1]
    count+=1
mze_tag_file = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_word_tag.csv','w')
mze_tag = csv.writer(mze_tag_file)
for key in word_tag_dict:
    mze_tag.writerow([key.encode('utf-8'),word_tag_dict[key]])

database_file.close()
mze_tag_file.close()


