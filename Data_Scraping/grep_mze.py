import requests
import csv 
from bs4 import BeautifulSoup
import re
import csv 
from nltk.stem import SnowballStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import RegexpTokenizer
from gensim import models, corpora
from nltk import word_tokenize
from nltk.corpus import stopwords



text_limit = 400
Volume = 10
Stuck = 3

mze = {(1,1):(3,113), (1,2):(3,119), (1,3):(3,133), (2,1):(3,129),
       (2,2):(3,133), (2,3):(3,127), (3,1):(3,128), (3,2):(3,127), (3,3):(3,124), (4,1):(3,129), 
       (4,2):(3,128), (4,3):(3,127), (5,1):(3,130), (5,2):(3,130), (5,3):(3,126), (6,1):(3,130), 
       (6,2):(3,114), (6,3):(3,128), (7,1):(3,130), (7,2):(3,130), (7,3):(3,129), (8,1):(3,122), 
       (8,2):(3,130), (8,3):(3,127), (9,1):(3,129), (9,2):(3,145), (9,3):(3,125), (10,1):(3,129), 
       (10,2):(3,129), (10,3):(3,148)}



gtoken = WordPunctTokenizer()
rtoken =  RegexpTokenizer(r'\w+')
gs = SnowballStemmer('german')
NUM_TOPICS = 10
STOPWORDS = stopwords.words('german')
Punctuations= [',','.',':','\"','\'','?','!']

def convert_num(s,digits):
    k  = 0
    s0 = s
    while s>0:
        k+=1
        s=s/10
    return '0'*(digits-k)+str(s0)

def stemmed_version(text):
    words = gtoken.tokenize(text)
    stemmed_words = [gs.stem(word) for word in words if not word in Punctuations]
    return (' '.join(stemmed_words),len(stemmed_words))

count = 0
article_count = 0
paragraph_style = ["indention"+str(i) for i in range(10)]+['']
cur_article = ''
original_cur_article = ''
outfile = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_whole_database.csv','w')
outfile_tsv = csv.writer(outfile,delimiter=',')
out_tm = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_whole_chunk.tsv','w')
out_tm_tsv = csv.writer(out_tm,delimiter='\t')
outfile_tsv.writerow(['index','article_index','vol','book','title','author','content','words'])


for vol in range(1,Volume+1):
    for book in range(1,Stuck+1):
        for page in range(mze[(vol,book)][0],mze[(vol,book)][1]):
            url = 'http://telota.bbaw.de/exist/servlet/db/mes/scripts/showPage.xql?volume='+str(vol)+'&part='+str(book)+'&page='+str(page)+'&qString=undefined#'
            response = requests.get(url)
            data = response.text
            soup = BeautifulSoup(data, 'html5lib')
            potential_content = soup.find_all(name=['h5','p'])
            for content in potential_content:
                if content.name=='p' and 'class' in content.attrs and set(content.attrs['class']).intersection(set(paragraph_style))!=set([]):
                    text = re.sub(re.compile('\s+'),' ', content.text)
                    (stemmed_text, num_words) = stemmed_version(text)
                    if paragraph_count <= text_limit:
                        cur_article+=stemmed_text+' '
                        original_cur_article+=text+' '
                        paragraph_count+=num_words
                    else:
                        outfile_tsv.writerow([count,article_count,vol,book, title.encode('utf-8','ignore'), author.encode('utf-8','ignore'),original_cur_article.encode('utf-8','ignore'),paragraph_count])
                        out_tm_tsv.writerow([count,'vol{0}book{1}article{2}'.format(vol,book,article_count),cur_article.encode('utf-8','ignore')])
                        paragraph_count = num_words
                        count+=1
                        cur_article = stemmed_text+' '
                        original_cur_article = text+' '
                if content.name=='h5':
                    if cur_article!='':
                        outfile_tsv.writerow([count,article_count,vol,book, title.encode('utf-8','ignore'), author.encode('utf-8','ignore'),original_cur_article.encode('utf-8','ignore'),paragraph_count])
                        out_tm_tsv.writerow([count,'vol{0}book{1}article{2}'.format(vol,book,article_count),cur_article.encode('utf-8','ignore')]) 
                    reference = soup.find(name='p', attrs={'class':'referenceLine'})
                    try:
                        reference_text = re.sub(re.compile('\s+'),' ',reference.text)
                    except AttributeError:
                        print (vol,book,page)
                    info = reference_text.split(':')
                    author = info[0]
                    title_info = info[1].split('Bd')[0]
                    title = re.sub(re.compile('[\<,\>]+'),'', title_info)
                    cur_article=''
                    original_cur_article = ''
                    count+=1
                    paragraph_count = 0
                    article_count+=1
                    print article_count
                    
outfile.close()
out_tm.close()


""" database format """
""" index article_index vol book  title author content num_words """
