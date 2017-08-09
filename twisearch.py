import tweepy
import json
import datetime

# Auth with twitter API
auth = tweepy.OAuthHandler('consumer_token', 'consumer_secret')
auth.set_access_token('key', 'secret')

api = tweepy.API(auth, wait_on_rate_limit=True)


# config
# keyword you want to search
hashtag = 'covfefe'
# lof file prefix
log_prefix = 'tp_log'
# filter with languages etc en,fa,...
lang = 'en'


# define
dt = str(datetime.datetime.utcnow().strftime("%d-%B-%Y %H:%M:%S"))
filename = log_prefix + '_' + hashtag
tw = []
pre_text = '\n\tstreaming ' + hashtag + ' and log in to ' + filename + '\n\t' + dt + '\n\n\n'
print(pre_text)


# write to file function
def filewrite(filename, mode, string):
    f = open(filename, mode)
    f.write(str(string))
    f.close()


# send pre_text to log
filewrite(filename, 'a', pre_text)


# streamer class
class MyStreamListener(tweepy.StreamListener):

    def on_data(self, data):
        # get twitte
        decoded = json.loads(data)

        # send to list
        tw.append(decoded['text'])

        res = str(len(tw)) + '::' + str(decoded['created_at']) + '\n' + 'username: ' + str(decoded['user']['screen_name']) + ' ' + '\n' + str(decoded['text']) + '\n\n'
        print(res)

        # write twitte info to log
        filewrite(filename, 'a', res)

        return True

    def on_status(self, status):
        # Error
        print('\n\t Error')
        print(status.text)
        filewrite(filename, 'a', status.text)


# define streamer
listener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=listener)

# filter stream
myStream.filter(track=[hashtag, '#'+hashtag], languages=[lang], async=True)
