""" part of the script is adapted from https://datascience.blog.wzb.eu/2016/07/13/accurate-part-of-speech-tagging-of-german-texts-with-nltk/"""

import nltk
import numpy as np 
from ClassifierBasedGermanTagger.ClassifierBasedGermanTagger import ClassifierBasedGermanTagger
import pickle

corp = nltk.corpus.ConllCorpusReader('.', 'tiger_release_aug07.corrected.16012013.conll09',['ignore', 'words', 'ignore', 'ignore', 'pos'], encoding='utf-8')
tagged_sents = corp.tagged_sents()
#random_perm = np.random.permutation(len(tagged_sents))
#tagged_sents = [tagged_sents[i] for i in random_perm]
#split_percentage = 0.1
#split_size = int(len(tagged_sents)*split_percentage)
#train_sents, test_sents = tagged_sents[split_size:],tagged_sents[:split_size]
tagger = ClassifierBasedGermanTagger(train=tagged_sents)
with open('nltk_german_classifier.pickle','wb') as f:
    pickle.dump(tagger,f,protocol=2)




