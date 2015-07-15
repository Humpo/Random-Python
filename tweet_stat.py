#!/usr/bin/env python
from __future__ import unicode_literals #this needs to be here

def module_exists(module_name):
        '''function to check if an import exists'''
        try:
            __import__(module_name)
        except ImportError:
            return False
        else:
            return True
####NOT TWEET_LEARN RELATED ABOVE####
'''class is not defined!!!!
class StdOutListener(StreamListener):
    def on_data(self, data):
        d = json.loads(data)
        retweets = d.get("retweet_count")
        #if retweets != 0 and retweets != None:
        print d.get("text")
        #print d.get("retweet_count") 
        return True
    def on_error(self, status):
        print status
'''
def regression(data):
    tw = zip(*tw)

    learning_X = tw[0]
    learning_X_temp = tw[0][::2] #<----- THE X DATA
    
    learning_Y = tw[1]
    learning_Y_temp = tw[1][::2] #<-----  The Y DATA

    learning_X_train = learning_X_temp[:-20] #<------
    learning_X_test = learning_X_temp[-20:]

    # Split the targets into training/testing sets
    learning_y_train = learning_Y_temp[:-20] #<--- train on the first 20
    learning_y_test =  learning_Y_temp[-20:] #<--- test myself on the last 20 (TWEET_SIZE, RETWEETS)

    regr = linear_model.LinearRegression()

    learning_X_train = [[i] for i in learning_X_train]
    learning_X_test = [[i] for i in learning_X_test]

    regr.fit(learning_X_train, learning_y_train)

   
    # The coefficients
    print 'Coefficients: \n', regr.coef_

    # Plot outputs
    plt.scatter(learning_X_test, learning_y_test,  color='black')
    plt.plot(learning_X_test, regr.predict(learning_X_test), color='blue',
         linewidth=3)
    
    plt.xticks(())
    plt.yticks(())

    plt.show()
        
def stream():

    consumer_key = 'zg9yQTGTT2oizk3XLMHGLzfpJ'
    consumer_secret = 'nmiwqRpWDX0oxTCUTro8sPeUVUXIZHW9O1VZcTb0mLyfHw51sc'
    access_token = '700001043-oxm3LZ72y4WmWGRqY66QjV0SzZoHGy5OGgwic26M'
    access_token_secret = 'hGJZWTb5bjGFSiuIQrff5UajKdlyXcp7Lyun5SJzq05Su'
    

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(locations=[-180,-90,180,90],languages = ['en'])

def pull():

    nicePrint = PrettyPrinter(indent=2, width=70)
    api = twitter.Api(consumer_key = 'zg9yQTGTT2oizk3XLMHGLzfpJ',
                      consumer_secret = 'nmiwqRpWDX0oxTCUTro8sPeUVUXIZHW9O1VZcTb0mLyfHw51sc',
                      access_token_key = '700001043-oxm3LZ72y4WmWGRqY66QjV0SzZoHGy5OGgwic26M',
                      access_token_secret = 'hGJZWTb5bjGFSiuIQrff5UajKdlyXcp7Lyun5SJzq05Su')

    #^Using twitter library we verify the app through the REST API with these keys
    
    user_info_dict = api.VerifyCredentials().AsDict()
    #^Gets my info as a dictonary

    #nicePrint.pprint(user_info_dict)
    #^isplay user info
    print('\n')
       

    current_tweets = api.GetHomeTimeline()
    current_tweets = [s.AsDict() for s in current_tweets]

    return current_tweets
    
    #nicePrint.pprint([s.AsDict() for s in current_tweets])
    #^gets all current tweets in timeline(home page), and prints it all out in dicts

    return 
    
def search():

    tw = []
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords([' ']) # let's define all search keywords - now, we want all tweets with a space in them
        tso.set_language('en') # we want to see english tweets only
        tso.set_include_entities(False) # and don't give us all those entity information
        ts = TwitterSearch(consumer_key = 'zg9yQTGTT2oizk3XLMHGLzfpJ',
                      consumer_secret = 'nmiwqRpWDX0oxTCUTro8sPeUVUXIZHW9O1VZcTb0mLyfHw51sc',
                      access_token = '700001043-oxm3LZ72y4WmWGRqY66QjV0SzZoHGy5OGgwic26M',
                      access_token_secret = 'hGJZWTb5bjGFSiuIQrff5UajKdlyXcp7Lyun5SJzq05Su')
        i = 0
        for tweet in ts.search_tweets_iterable(tso):
            #if (tweet['retweet_count'] != 0):
            #tw.append((len(tweet['text'].split()), tweet['retweet_count']))
            #print(str(i))
            #backspace(len(str(i)))
            tw.append(tweet)
            if i == 300:
                break
            i += 1
        return tw
            #print tw
            #print( '%s: @%s tweeted: %s' % ( tweet['retweet_count'], tweet['user']['screen_name'], tweet['text'] ) )
            # print # of retweents, tweeter, and content of tweet
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

def main():
    nicePrint = PrettyPrinter(indent=2, width=70)

    tw = [None]
    #tw = pull()
    tw = search() 
    #stream()
    
    nicePrint.pprint(tw[0])

    tweet=tw[0]

    text = tweet['text']
    
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F680-\U0001F6FF'
            u'\u2600-\u26FF\u2700-\u27BF]+', 
            re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
            u'\ud83c[\udf00-\udfff]|'
            u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            u'[\u2600-\u26FF\u2700-\u27BF])+', 
            re.UNICODE)
    
    text = ''.join([ud.name(char) if myre.sub('',char) == '' else char for char in text])
        
    print text
    
    analysis = twitter.parse_tweet.ParseTweet(tweet['user']['name'], text)

    text = ''.join(ch for ch in text if ch.isalnum() or ' ')

    print '\n\n'
    print text.encode('utf-8')
    print '\n'
    for i in str(analysis).split(', '):print i
    print "Favorites: %d" % (tweet['favorite_count'])
    print "Retweets: %d" % (tweet['retweet_count'])
    print "Words: %d" % (len(text.split()))
    print "Word Length Avg: %f" % (sum([len(w) for w in text.split()]) / len(text.split()))

    letters = ' '.join([' '.join(c) for c in text.split()])

    fdist = nltk.FreqDist(letters)
    
    print "Most common: "
    print fdist.plot(50,cumulative=False)
        

if __name__ == "__main__":
    #^This should be the first thing that is checked in the program
    '''
    This program utilizes several python data analytic modules for processing tweets
    '''

    import collections
    import re
    from pprint import PrettyPrinter
    import json
    import sys
    import string
    import unicodedata as ud
    #^default imports that should come with python

    Requirements = ['nltk', 'tweepy','TwitterSearch','python-twitter','scikit-learn', 'numpy', 'matplotlib']#add import requirements here

    imported = False #Import flag to make sure things are import correctly
    installed = False #Installed flag to make sure things are installed

    while not imported:
        try:#tries to import the necessary stuff you want
            
            from tweepy.streaming import StreamListener
            from tweepy import OAuthHandler
            from tweepy import Stream
            from TwitterSearch import *
            import matplotlib.pyplot as plt
            import numpy as np
            from sklearn import datasets, linear_model
            import twitter
            import twitter.parse_tweet
            import nltk
            #put what you want imported and stuff here
            #MAKE SURE TO ADD TO REQUIREMENTS

            imported = True #at this point everything should be imported
        except:#UH-OH something isn't downloaded!!! Time to check requirements
            if not installed:
                import os, pip #stuff to import more stuff
                from setuptools.command import easy_install

                pip_args = [ '-v' ]#gives uber output also creating pip command
                pip_args.append('install')#install command
                pip_args.append('-U')#install command
                for req in Requirements: #adds the requirements
                    pip_args.append( req )

                print("You do not have the proper modules needed.")
                print("May I install them? (y/n)")

                answer = str(raw_input(">>> ")).lower()
                while (answer != 'y') and (answer != 'n'):
                    print("I don't undestand")
                    answer = str(raw_input("May I install it for you (Y/N)\n>>> ")).lower()

                if answer[0].lower() == 'y':
                    print('Installing requirements: ' + str(Requirements) + "and scipy")

                    pip.main(['install','--upgrade', 'pip'])

                    if not module_exists('scipy'):
                        print 'need scipy to continue. Get at'
                        print 'http://sourceforge.net/projects/scipy/files/scipy/0.15.0/scipy-0.15.0-win32-superpack-python2.7.exe/download'
                    if pip.main(pip_args) == 0:
                        installed = True
                    elif easy_install.main(['-U',pip_args]):
                        installed = True
                    else:
                        break
                else:
                    break
            else:
                break
            
    if imported:
        main()
    else:
        print("Invalid Import or requirement listed")
