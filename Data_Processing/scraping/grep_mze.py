import requests
import csv 
from bs4 import BeautifulSoup
import re
import csv
from nltk.tokenize import WordPunctTokenizer



text_limit = 400
Volume = 10
Stuck = 3

mze = {(1,1):(3,113), (1,2):(3,119), (1,3):(3,133), (2,1):(3,129),
       (2,2):(3,133), (2,3):(3,127), (3,1):(3,128), (3,2):(3,127), (3,3):(3,124), (4,1):(3,129), 
       (4,2):(3,128), (4,3):(3,127), (5,1):(3,130), (5,2):(3,130), (5,3):(3,126), (6,1):(3,130), 
       (6,2):(3,114), (6,3):(3,128), (7,1):(3,130), (7,2):(3,130), (7,3):(3,129), (8,1):(3,122), 
       (8,2):(3,130), (8,3):(2,127), (9,1):(3,129), (9,2):(3,145), (9,3):(3,125), (10,1):(3,129), 
       (10,2):(3,129), (10,3):(3,148)}

gtoken = WordPunctTokenizer()
Punctuations= [';','+','{','}','...','*','&','-','(',')','<','>','[',']','\'','\"',':',',','.','?','!'] 

def convert_num(s,digits):
    """ output index format """
    k  = 0
    s0 = s
    while s>0:
        k+=1
        s=s/10
    return '0'*(digits-k)+str(s0)

def token_count(text):
    """ stem the german text based on nltk.SnowballStemmer """
    words = gtoken.tokenize(text)
    words = [word for word in words if not word in Punctuations]
    return len(words)

def no_title_criteria(soup):
    """ dealing with the case when there is only h3, but no h5 in the html page """
    """ h3 tag is only picked up if there are paragraphs underneath, and it is not picked up otherwise """
    content_order = []
    potential_content = soup.find_all(name=['h3','p'])
    for content in potential_content:
        if content.name == 'h3':
            content_order.append('h3')
        if content.name=='p' and 'class' in content.attrs and set(content.attrs['class']).intersection(set(paragraph_style))!=set([]):
            content_order.append('paragraph')
    index = 0
    while index < len(content_order) and content_order[index]!='h3':
        index+=1
    if content_order[index+1:]!=[]:
        return True
    else:
        return False

def author_extraction(author):
    if '=' in author:
        pattern = re.compile('\<\=([\s\S]+)\>')
        author_name = re.findall(pattern,author)
        author_name = author_name[0].strip('\? ')
    else:
        author_name = re.sub('[\<\>]+','',author)
    return author_name

count = 0
article_count = 0
paragraph_style = ["indention"+str(i) for i in range(10)]+['']
original_cur_article = ''
outfile = open('/Users/Wei/Documents/Technique_Study/Coding/LeetCode/MZE/Data/mze_whole_database.csv','w')
outfile_tsv = csv.writer(outfile,delimiter=',')
outfile_tsv.writerow(['index','article_index','vol','book','title','author','content','words'])

written = set([])
for vol in range(1,Volume+1):
    for book in range(1,Stuck+1):
        for page in range(mze[(vol,book)][0],mze[(vol,book)][1]+1):
            url = 'http://telota.bbaw.de/exist/servlet/db/mes/scripts/showPage.xql?volume='+str(vol)+'&part='+str(book)+'&page='+str(page)+'&qString=undefined#'
            response = requests.get(url)
            data = response.text
            soup = BeautifulSoup(data, 'html5lib')
            potential_content = soup.find_all(name=['h5','p'])
            no_title_indicator = False
            if soup.find_all(name=['h3'])!=[] and soup.find_all(name=['h5'])==[] and soup.find_all(name=['p'],attrs={'class':re.compile('indention[0-9]| ')})!=[]:
                no_title_indicator = no_title_criteria(soup)
            for content in potential_content:
                if content.name=='p' and 'class' in content.attrs and set(content.attrs['class']).intersection(set(paragraph_style))!=set([]):
                    text = re.sub(re.compile('\s+'),' ', content.text)
                    num_words = token_count(text)
                    if paragraph_count + num_words <= text_limit:
                        original_cur_article+=text+' '
                        paragraph_count+=num_words
                    else:
                        outfile_tsv.writerow([count,article_count,vol,book, title.encode('utf-8','ignore'), author.encode('utf-8','ignore'),original_cur_article.encode('utf-8','ignore'),paragraph_count])
                        paragraph_count = num_words
                        count+=1
                        original_cur_article = text+' '
                if content.name=='h5' or no_title_indicator:
                    if original_cur_article!='':
                        actual_book = book
                        actual_vol = vol
                        if not (vol,book) in written:
                            written.add((vol,book))
                            if book in [2,3]:
                                actual_book=book-1
                                actucal_vol = vol
                            if  book ==1 and vol>1:
                                actual_book=3
                                actual_vol = vol-1
                        outfile_tsv.writerow([count,article_count,actual_vol,actual_book, title.encode('utf-8','ignore'), author.encode('utf-8','ignore'),original_cur_article.encode('utf-8','ignore'),paragraph_count])
                    if no_title_indicator:
                        author = 'Editor'
                        title = 'Section Preface'
                        no_title_indicator = False
                    else:
                        reference = soup.find(name='p', attrs={'class':'referenceLine'})
                        try:
                            reference_text = re.sub(re.compile('\s+'),' ',reference.text)
                        except AttributeError:
                            print (vol,book,page)
                        info = reference_text.split(':')
                        author = info[0]
                        author = author_extraction(author)
                        title_info = info[1].split('Bd')[0]
                        title = re.sub(re.compile('[\<,\>,\),\*]+'),'', title_info)
                    original_cur_article = ''
                    count+=1
                    paragraph_count = 0
                    article_count+=1
                    print article_count
                    
outfile.close()


""" database format """
""" index article_index vol book  title author content num_words """
