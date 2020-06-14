import tweepy
import pandas as pd

consumer_key = "83ZNOt8QUIhp6mOHdhYMYKnmg"
consumer_secret = "mxJcrKl7iOqIG3AM1Fv4r4J5hP9rsWYLTm2d88VFVGlsnWg2jT"
access_token = "77437868-NN1FeB3Cxnk4JlxS8ObDGV95jWg8oAOoLonktrQuO"
access_token_secret = "YaeLO2YJMmRSk4O0FRFIGo0nKo4cGd3Ntso8lE80Z9Uy4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

tweetan=[]
tanggal=[]
teks=[]
Id=[]
sn=[]
source=[]
rtc=[]

for tweet in tweepy.Cursor(api.search, q = "#DiRumahAja", 
                           geocode ="-6.21839,106.90801,7km", 
                           count = 200,
                           lang = "id",since="2020-03-02").items(10000):
    if not tweet : 
        print('tweet habis')
        break
    print(tweet.created_at, tweet.text)
    tweetan.append(tweet)
    tanggal.append(tweet.created_at) 
    teks.append(tweet.text.encode("utf-8"))
    Id.append(tweet.id)
    sn.append(tweet.user.screen_name)
    source.append(tweet.source)
    rtc.append(tweet.retweet_count)


data_json = pd.DataFrame(tweetan)
data_json.to_json('Crawling Twitter.json')
data = pd.DataFrame()
data['Tanggal']=tanggal
data['Tweets']=teks
data['ID']=Id
data['Screen Name']=sn
data['Banyak Retweet']=rtc
data['Source']=source
data.to_csv('Crawling Twitter.csv',index=False)