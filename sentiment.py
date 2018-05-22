#library
import numpy as np                 #محاسبات عددی
import pandas as pd         #برای رسیدگی به داده ها
import tweepy               #برای فراخانی api توییتر
from textblob import TextBlob   #برای تحلیل داده ها
import tkinter
import re                   #Regular Expression

print("سلام کاربر عزیز \n این اسکریپت تحلیل احساسات (پردازش زبان طبیعی)هستش \n"
      "فقط کافیه ایدی یا یوز فردی در توییتر را وارد  کنید "
      "تا اسکریپت شروع به تحلیل تویت ها کند و نموداری کامل از لایک ها ری توییت ها و همچینین مثبت یا منفی بودن توییت ها در اختیار شما قرار بدهد\n"
      "این اسکریپت در ابتدای کار قرار دارد جهت همکاری و توصعه به ادرس vx90 در گیت هاب مراجعه فرمایید .محمد حسینی فر'\n"
      )
#برای تطبیق و تجسم

from IPython.display import display
import matplotlib.pyplot as plt


#کلیدهای دسترسی توییتر

# Consume:
CONSUMER_KEY=''
CONSUMER_SECRET=''

# Access:
ACCESS_TOKEN=''
ACCESS_SECRET=''


#راه اندازی api توییت#



def twitter_api():
    # # تأیید اعتبار و دسترسی با استفاده از کلید
    auth =tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
    #API بازگشت با احراز هویت
    api = tweepy.API(auth)
    return api





#شیء استخراج را ایجاد می کنیم

extractor=twitter_api()



#استخراج توییت های یوزر خاص

#user=input("یوز را وارد کنید:")

user=input("نام کاربری یا ایدی فرد را وارد کنید:")

#تعداد توییت ها
count=int(input("تعداد توییت های مورد برسی را وارد کنید:"))





#یک لیست از توییت ها ایجاد میکنیم

tweets=extractor.user_timeline(screen_name=user, count=count)
print("تعداد توییت های استخراج شده: {}.\n".format(len(tweets)))

#ده توییت اخر را چاپ میکنیم
def top10():
 print("۱۰ توییت اخر")
 for tweet in tweets[:10]:
    print(tweet.text)
    print()
 return


#یک فرم اطلاعات با پاندا ایجاد میکنیم

data=pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])


display(data.head(20))   #نمایش ۲۰ ستون اول توییت ها

#نمایش ویژگی های رشته
#print(dir(tweets[0]))

#اضافه کردن ستون و سطر به پاندا

#print(tweets[0].id)


data['len']=np.array([len(tweet.text) for tweet in tweets])
data['ID']=np.array([tweet.id for tweet in tweets])
data['Date']=np.array([tweet.created_at for tweet in tweets])
data['Source']=np.array([tweet.source for tweet in tweets])
data['Likes']=np.array([tweet.favorite_count for tweet in tweets])
data['RTs']=np.array([tweet.retweet_count for tweet in tweets])

display(data.head(10))


#محاسبه لایک و ری توییت ها با numpy
leen=np.mean(data['len'])

print(" میانگین طول کارکتر ها: {}".format(leen))
#بیشترین لایک و ری توییت
l_max=np.max(data['Likes'])
r_max=np.max(data['RTs'])

def biiger():
  like=data[data.Likes==l_max].index[0]
  rt=data[data.RTs==r_max].index[0]

#بیشترین لایک
  print("توییت با بیشترین لایک: \n{}".format(data['Tweets'][like]))

  print("تعداد لایک: {}".format(l_max))

  print("{} تعداد کارکتر.\n".format(data['len'][like]))

  print("#################################################################")
#بیشترین ری توییت
  print("توییت با بشترین ری توییت: \n{}".format(data['Tweets'][rt]))

  print("تعداد ری توییت: {}".format(r_max))

  print(" تعداد کارکتر ها:{}\n".format(data['len'][rt]))

  print("##################################################################")

#اضافه کردن به نمودار و پاندا
  n_len=pd.Series(data=data['len'].values, index=data['Date'])
  n_like=pd.Series(data=data['Likes'].values, index=data['Date'])
  n_re=pd.Series(data=data['RTs'].values, index=data['Date'])


  n_len.plot(figsize=(20,5), color='b')

  plt.show()
  n_like.plot(figsize=(20,5), label="likes", legend=True)
  plt.show()
  n_re.plot(figsize=(16,4), label="re", legend=True)
  plt.show()

  return




sources = []
for source in data['Source']:
    if source not in sources:
        sources.append(source)

# دیوایس سورس :

print("Creation of content sources:")
for source in sources:
    print("* {}".format(source))


percent = np.zeros(len(sources))

for source in data['Source']:
    for index in range(len(sources)):
        if source == sources[index]:
            percent[index] += 1
            pass

percent /= 100

# چارت و نمودار کردن
def base():
   base=pd.Series(percent, index=sources, name='Sources')
   base.plot.pie(fontsize=11, autopct='%.2f', figsize=(6, 6))
   plt.show()
   return



#قسمت اصلی  اول  کاراکتر ها رو با رگ پاک میکنیم
import re

def remove_sc(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
#قسمت جالب  تحلیل  با این چند خط کد انجام میشه
def analize_sentiment(tweet):

    analysis = TextBlob(remove_sc(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1
data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])

# We display the updated dataframe with the new column:
display(data.head(10))


pos_tweets =[tweet for index,tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
neu_tweets =[tweet for index,tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
neg_tweets =[tweet for index,tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]





print("درصد تویت های مثبت: {}%".format(len(pos_tweets)*100/len(data['Tweets'])))
print("درصد تویت های طبیعی: {}%".format(len(neu_tweets)*100/len(data['Tweets'])))
print("درصد تویت های منفی: {}%".format(len(neg_tweets)*100/len(data['Tweets'])))


analize=[(len(pos_tweets)*100/len(data['Tweets'])),(len(neg_tweets)*100/len(data['Tweets'])),(len(neu_tweets)*100/len(data['Tweets']))]
sentiment=pd.Series(analize)
#print(cc)
def pie():
  plt.axes(aspect=1)
  plt.title("sentiment analysis")
  plt.pie(sentiment,labels=("positive","negative",'neutral'),autopct='%.2f')
  plt.show()
  return
print("برای نمایش ۱۰ توییت اخر عدد ۱ \n"
      "برای نمایش سورس نویسنده توییت هاعدد ۲ \n"
      "برای نمایش نمودار کامل بیشترین لایک و ری توییت عدد ۳ \n"
      "برای نمایش چارت و نمودار تحلیل احساسات عدد ۴ \n"
      "برای نمایش همه موارد به ترتیب عدد ۵ را وارد کنید")
bigger = input(":")
if bigger == '3‍':
  biiger()
elif bigger=='2':
    base()
elif bigger=="1":
    top10()
elif bigger=='4':
    pie()
elif bigger=='5':
    pie()
    base()
    top10()
    biiger()

else:
  print("ok")
