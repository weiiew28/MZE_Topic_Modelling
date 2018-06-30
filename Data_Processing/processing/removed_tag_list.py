# -*- coding: utf-8 -*- 
import csv
import collections

removal_tag_list = ['ART', 'ITJ', 'KON', 'KOKOM', 'KOUI', 'KOUS', 'PAV', 'PAVREL', 'PDAT', 'PDS', 'PRELAT', 'PRELS', 'PTKA', 'PWAT', 'PWAV', 'PWAVREL', 'PWREL', 'VAINF']

vocab_file = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_word_tag.csv','r')
vocab = csv.reader(vocab_file)
removed_vocab_file = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_word_removed.csv','w')
removed_vocab = csv.writer(removed_vocab_file)
keep_vocab_file = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_word_keep.csv','w')
keep_vocab = csv.writer(keep_vocab_file)

vocab_dict = collections.defaultdict(str)
for line in vocab:
    vocab_dict[line[0].decode('utf-8')] = line[1]
    if line[1] in removal_tag_list:
        removed_vocab.writerow([line[0]])
    else:
        keep_vocab.writerow([line[0]])

vocab_file.close()
removed_vocab_file.close()
keep_vocab_file.close()
