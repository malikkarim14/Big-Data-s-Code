from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import word_tokenize 
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import csv
import re


# Text Cleasing Function
def my_preprocessor(mytext):
    #Convert to lower case
    mytext = mytext.lower()
    #Convert www.* or https?://* to URL
    mytext = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',mytext) 
    #Convert @username to AT_USER
    mytext = re.sub('@[^\s]+','AT_USER',mytext)
    #Remove additional white spaces
    mytext = re.sub('[\s]+', ' ', mytext)
    #Replace #word with word
    mytext = re.sub(r'#([^\s]+)', r'\1',mytext)
    #trim
    mytext = mytext.strip('\'"')
    return mytext

# Tokenization & Stemming Function
def my_tokenizer(mytext):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    mytext = stemmer.stem (mytext)
    words = word_tokenize(mytext)
    tokens=[]
    for w in words:
        #replace two or more with two occurrences 
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL) 
        w = pattern.sub(r"\1\1", w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet or number 
        val = re.search(r"^[a-zA-Z0-9][a-zA-Z0-9-]*$", w)
        #add tokens
        if(w in ['b','rt','at','user','url'] or val is None or len(w) <= 3):
            continue
        else:
            tokens.append(w)
    return tokens

#List of Stop Words
factory2 = StopWordRemoverFactory()
stopwords = factory2.get_stop_words()

# Load the Blog article
data = pd.read_csv(open(r"D:\Kuliah\Big Data\Merge\CrawlingJaktim.csv"))
file = data['Tweets'].tolist()

# Word Vectorization
print("Memulai proses vektorisasi kata...")
vectorizer_count = CountVectorizer(preprocessor=my_preprocessor,tokenizer=my_tokenizer, stop_words=stopwords,min_df=2,max_df=0.95)
vectorizer_tfidf = TfidfVectorizer(preprocessor=my_preprocessor,tokenizer=my_tokenizer, stop_words=stopwords,min_df=2,max_df=0.95)
word_count = vectorizer_count.fit_transform(file)
word_tfidf = vectorizer_tfidf.fit_transform(file)

# mapping from column index to feature name
nama_fitur = vectorizer_tfidf.get_feature_names()

# Penentuan jumlah artikel dan fitur
dimensions = word_count.get_shape()
print("Jumlah artikel = %s" % dimensions[0])
print("Jumlah fitur = %s" % dimensions[1])

# Penentuan jumlah kata pada artikel terpanjang & terpendek (pada artikel yg telah dilakukan preprocessing & filtering)
jumlah_kata_per_artikel = word_count.sum(axis=1)
print("Jumlah kata pada artikel terpanjang = %s" % str(max(jumlah_kata_per_artikel)).strip('[]'))
print("Jumlah kata pada artikel terpendek = %s" % str(min(jumlah_kata_per_artikel)).strip('[]'))

# Penentuan 1 kata dan 10 kata dengan bobot tfidf tertinggi pada setiap artikel
print ("Memulai proses penentuan 1 kata dengan bobot tertinggi pada setiap artikel...")
n = 0
content1 = []
content2 = []
for n in range(0,dimensions[0]): 
    # convert sparse matrix row by row #
    row = word_tfidf.getrow(n).toarray()[0].ravel()
    # sort to identify 10 top values and its indexes #
    top_ten_indices = row.argsort()[-10:]
    top_ten_values = row[row.argsort()[-10:]]
    # identify the highest TFIDF value and word #
    highestTFIDFword = nama_fitur[top_ten_indices[9]]
    highestTFIDFvalue = top_ten_values[9]
    top1word = {'nomor artikel': n+1, 'nilai TFIDF': highestTFIDFvalue,'top word':highestTFIDFword}
    content1.append(top1word) 
    content2.append(highestTFIDFword)

#Membuat plot kata tersering disebut
content2 = np.array(content2)
words, n = np.unique(content2, return_counts=True)

data = pd.DataFrame()
data['word'] = words
data['freq'] = n
data = data.sort_values(by='word', ascending=False)
data = data.loc[data['freq'] >= 110]

plt.figure(figsize = (10,10))
sns.barplot(x = data['word'],y = data['freq'])
for i, v in enumerate(data['freq'].tolist()):
    if i == 0 : i-=0.1
    plt.text(i-.3, v + 11, str(v),fontsize=11)
plt.title('Kata Paling Sering Disebut',fontsize=20)
plt.xticks(rotation=90)
plt.xlabel('Kata',fontsize=16)
plt.ylabel('Frekuensi',fontsize=16)
plt.show()


# Merekam kata dengan nilai TFIDF tertinggi pada setiap artikel 
filetarget1 = 'Top_word_Jaktim.csv'
with open(filetarget1, 'w') as file_object1:
    writer = csv.writer(file_object1)
    writer.writerow(content1)

file_object1.close()

print ("Prosess telah selesai!")

# End Program