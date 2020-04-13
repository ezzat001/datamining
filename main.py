from monkeylearn import MonkeyLearn # Importing the AI API
from monkeylearn.exceptions import PlanQueryLimitError
from twitter_scraper import get_tweets # Importing the Twitter Scraper
import random
positive = []
negative = []
neutral = []
all = []
tokens = []
file = open('tokens.txt','r')

for i in file.readlines():
    i=i.replace('\n','')
    tokens.append(i)

#Twitter Accounts to fetch tweets from them
celeb = ['Tumharaabbu', 'GuyKawasaki', 'PPathole', 'Damian702' , 'elonmusk' , 'LeoDiCaprio',
'needvcillian', 'BillClinton', 'realDonaldTrump', 'HillaryClinton', 'BarackObama', 'garyvee',
'joshgondelman','FilthyRichmond','bobbyfinger','mindykaling']

data = []
print("Fetching",len(celeb),"celebrity...\n")
c = 0
#Fetching all of these celebrities tweets
for celebrity in celeb:
    c+=1
    print("Fetching",'#'+str(c),celebrity)

    for tweet in get_tweets(celebrity, pages=5):
        data.append(tweet['text'])

print()
print("Fetched","All","Tweets")
print('\n')
random.shuffle(data) # Shuffling the Tweets to get random insights
print("Take in Consideration that if you entered a big number it will take much time processing")
print("Recommended Number to input: 100")
print("Minimum Number to input: 1")
print("Maximum Number to input: 1000")
while True: # Getting input number to fetch tweets
    num = int(input("Enter the number of tweets you want: "))
    if num > 1000:
        print("It's Above than Maximum")
    elif num < 1:
        print("It's Lower than Minimum")
    else:
        break

counter = num
for tweet in data:
    if counter ==0:
        break
    for token in tokens:
        try:
            ml = MonkeyLearn(token)
            result = ml.classifiers.classify(model_id = 'cl_pi3C7JiL', data=[tweet])
            response = result.body
            i = response[0]
            text = i['text']
            i = i['classifications'][0]
            classf = i['tag_name']
            perc = i['confidence']*100
            perc = round(perc,1)
            if classf == 'Positive':
                lis = (text,perc)
                positive.append(lis)
            elif classf =="Neutral":
                lis = (text,perc)
                neutral.append(lis)
            elif classf =="Negative":
                lis = (text,perc)
                negative.append(lis)
            print(classf+':',str(perc)+'%')
        except PlanQueryLimitError as e:
            # No monthly queries left
            # e.response contains the MonkeyLearnResponse object
            print("Token is unusable switching to next")
            tokens.remove(token)
        break
    counter-=1

#Printing the Result Percentage
print()
print("Total Tweets:\n"+str(num))
print()
print("Positive Tweets:\n"+str(len(positive)),str((len(positive)/num)*100)+"%")
print("Negative Tweets:\n"+str(len(negative)),str((len(negative)/num)*100)+"%")
print("Neutral Tweets:\n"+str(len(neutral)),str((len(neutral)/num)*100)+"%")
