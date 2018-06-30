# -*- coding: utf-8 -*- 
import csv
from nltk.stem import SnowballStemmer
from nltk.tokenize import WordPunctTokenizer
import collections

database_file = open("/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_whole_database.csv",'r')
database = csv.reader(database_file)
keep_word_dict = collections.defaultdict(int)
count = 0
gtoken = WordPunctTokenizer()
gs = SnowballStemmer('german')
punctuations = [';','+','{','}','...','*','&','-','(',')','<','>','[',']','\'','\"',':',',','.','?','!']

vocab_file = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_word_keep.csv','r')
vocab = csv.reader(vocab_file)
for line in vocab:
    keep_word_dict[line[0].decode('utf-8')] = 1
vocab_file.close()

for line in database:
    if count!=0:
        print count
        index = line[0]
        content = line[-2].strip()
        tokenized_text = gtoken.tokenize(content.decode('utf-8'))
        tokenized_text_clean = [gs.stem(word) for word in tokenized_text if not word in punctuations and word in keep_word_dict]
        outfile = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/Corpus/{0}.txt'.format(int(index)),'w')
        text = ' '.join(tokenized_text_clean)
        outfile.write(text.encode('utf-8'))
        outfile.close()
    count+=1

        
