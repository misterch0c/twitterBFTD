#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2017 @misterch0c

# This program is free software: you can redistribute it and/or modify
# it under the terms of the HTL Hodge Twins License as published by
# the Free Gains Foundation, version 1 and only of the License.
#
# This program is distributed in the hope that you do whatever the FUCK,
# you wanna do with it


import tweepy
import time
import threading
import sys
import re
import pythonwhois
from secrets import consumer_key, consumer_secret, access_token, access_token_secret


class myThread (threading.Thread):
    def __init__(self,accounts):
        threading.Thread.__init__(self)
        self.accounts=accounts
    def run(self):
        print "Starting " + self.name
        findem(self.accounts)

def get_all_tweets(screen_name):
	alltweets = []
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	alltweets.extend(new_tweets)
	oldest = alltweets[-1]['id'] - 1
	while len(new_tweets) > 0:
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1]['id'] - 1
		print "...%s tweets downloaded so far for %s" % ((len(alltweets)),"@"+screen_name)
	return alltweets


def is_not_registred(url):
	try:
		who=pythonwhois.get_whois(url)
		return 'NOT FOUND' in str(who)

	except Exception:
		print('oops')
		return False

def get_accounts():
	acc=[]
	with open('accounts_leftover') as f:
		for l in f.readlines():
			twit_name=l.split(',')[0]
			acc.append(twit_name)
		return acc


def findem(accounts):
	urls=[]
	print('++ new thread ++')
	lock.acquire()
	if len(accounts) == 0:
		print("++ OVER ++")
		lock.release()
		return
	acc = accounts.pop(0)
	lock.release()
	tweets=get_all_tweets(acc)
	for tweet in tweets:
		if 'RT' not in tweet['text']:
			nn=tweet['entities']['urls']
			for ur in nn:
				expanded_url=ur["expanded_url"]
				expanded_url = expanded_url.replace("http://","").replace("https://","").replace("www.", "").split("/")[0].split(".")
				expanded_url = expanded_url[len(expanded_url)-2:len(expanded_url)]
				expanded_url = '.'.join(x for x in expanded_url)
				if expanded_url.lower() not in excluded:
					print("["+acc+"]"+"  --  "+ expanded_url)
					if is_not_registred(expanded_url):
						print("PWND " + acc +" --  "+expanded_url)
						urls.append(expanded_url)
	thread1=myThread(accounts)
	thread1.daemon=True
	thread1.start()
	f = open('BFTD_results.txt', 'a')
	f.write(str(urls) + acc +'\n')
	f.close() 
	print("+++ " +str(len(urls))+ " available domain found +++")
	print(urls)		


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())

#Let's assume those are registred.
excluded=['twitter.com','facebook.com','fb.me','apple.com','apple.co','snapchat.com','billboard.com','youtube.com','youtu.be','spotify.com','github.com','yahoo.com','fbi.gov','goo.gl','instagram.com','buzzfeed.com','amazon.com','vine.co','twimg.com','persiscope.tv','microsoft.com','fb.on','bit.ly','nike.com']
accounts=get_accounts()
lock = threading.Lock()

for x in range(20):
	print(x)
	thread1=myThread(accounts)
	thread1.daemon=True
	thread1.start()

while True:
	time.sleep(1)
	

