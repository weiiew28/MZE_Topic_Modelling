"german_pos_classifier.py" produces a classifer for German Part of Speech (POS) tagging. Reference: https://datascience.blog.wzb.eu/2016/07/13/accurate-part-of-speech-tagging-of-german-texts-with-nltk/
"mze_word_tag.py" creates a csv file of the (word,tag) pair from our mze database
"removed_tag_list.py" creates csv files for keep words and removed words based on POS criteria. We currently remove word that has POS: ART, ITJ, KON, KOKOM, KOUI, KOUS, PAV, PAVREL, PDAT, PDS, PRELAT, PRELS, PTKA, PWAT, PWAV, PWAVREL, PWREL, VAINF
"generate_clean_txt.py" generates txt file for the each text segment in the mze database. We first remove the word that has POS in the above removal list and then stem the word.    
