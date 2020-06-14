from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import re
import json

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

# Tokenization & Lemmatization Function
def my_tokenizer(mytext):
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
        if(w in ['AT_USER','URL'] or val is None):
            continue 
        else:
            #lemmatization
            w = WordNetLemmatizer().lemmatize(w) 
            tokens.append(w.lower())
        return tokens

#List of Stop Words
my_stop_words = ENGLISH_STOP_WORDS.union(['rt'])

# Load the Blog article
data_file = json.loads(open("D:/Kuliah/Big Data/News.json").read())
data = []
for i in range(len(data_file)):
    data.append(data_file[i]['content'])

# Word Vectorization
print("Memulai proses vektorisasi kata...")
vectorizer_count = CountVectorizer(preprocessor=my_preprocessor,tokenizer=my_tokenizer, stop_words=my_stop_words,min_df=2,max_df=0.95)
vectorizer_tfidf = TfidfVectorizer(preprocessor=my_preprocessor,tokenizer=my_tokenizer, stop_words=my_stop_words,min_df=2,max_df=0.95)
word_count = vectorizer_count.fit_transform(data)
word_tfidf = vectorizer_tfidf.fit_transform(data) 

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
print ("Memulai proses penentuan 1 kata dan 10 kata dengan bobot tertinggi pada setiap artikel...")
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
    # identify top 10 TFIDF values and words #
    m = 0
    top10words = []
    for m in range(0,10):
        word = nama_fitur[top_ten_indices[9-m]]
        top10words.append(word) 
        m = m + 1
    top10highestTFIDFword = {'nomor artikel': n+1, 'top 10 words': top10words}
    content2.append(top10highestTFIDFword)
    n = n +1


# Merekam kata dengan nilai TFIDF tertinggi pada setiap artikel 
filetarget1 = 'Top_word_in_each_news_article.json'
with open(filetarget1, 'w') as file_object1:
    json.dump(content1, file_object1)

# Merekam 10 kata dengan nilai TFIDF tertinggi pada setiap artikel
filetarget2 = 'Top_10words_in_each_news_article.json'
with open(filetarget2, 'w') as file_object2:
    json.dump(content2, file_object2) 

file_object1.close()
file_object2.close()

print ("Prosess telah selesai!")

# End Program
