#!/usr/bin/env python

import time
from getpass import getpass
from textwrap import TextWrapper

f= open('../results/workfile','a+')

import tweepy


class StreamWatcherListener(tweepy.StreamListener):


    status_wrapper = TextWrapper(width=120, initial_indent='    ', subsequent_indent='    ')

    def on_status(self, status):
        try:
            #print self.status_wrapper.fill(status.text)
            #print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)

            author = str(status.author.screen_name)
            f.write(author)
            f.write(' said: \t')
            f.write(self.status_wrapper.fill(status.text))
            f.write('\n')
            
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


def main():
    # Prompt for login credentials and setup stream object
    consumer_key = '0gU0QlrtKLlcidfyfVdH7R1qz'
    consumer_secret = '2GQ8jCjP58xu7gENWwmCTy4vVLRFsvzM2VJL1u7fHcumMqP4qA'
    access_token = '2585785981-kfCNAtFtgESI8sT3jw0AhH7qQ6UCdgk4HsWp2If'
    access_token_secret = 'PdATAHsTcnjX9gCgoCVMFcMuffTf3648JHHWC8vhSRQ7z'

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)

    # Prompt for mode of streaming
    valid_modes = ['sample', 'filter']
    mode = 'filter'

    if mode == 'sample':
        stream.sample()

    elif mode == 'filter':
#        follow_list = raw_input('Users to follow (comma separated): ').strip()
#        track_list = raw_input('Keywords to track (comma seperated): ').strip()
        follow_list = None
        track_list = ['%d years old'%year for year in range(1,51)]

        if follow_list:
            follow_list = [u for u in follow_list.split(',')]
            userid_list = []
            username_list = []
            
            for user in follow_list:
                if user.isdigit():
                    userid_list.append(user)
                else:
                    username_list.append(user)
            
            for username in username_list:
                user = tweepy.API().get_user(username)
                userid_list.append(user.id)
            
            follow_list = userid_list
        else:
            follow_list = None
        print follow_list
        stream.filter(follow_list, track_list)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'

