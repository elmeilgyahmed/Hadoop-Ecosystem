#!/usr/bin/python3

from collections import Counter
import sys
topic = None
word_upvotes = None
# here count will be initilzed to zeros we will use Counter object
count = Counter()  
##initalize the counter to count the upvotes
count_upvotes = 0
word_counting = 0
for line in sys.stdin:
    key, value = line.strip().split("\t")
    # because strip function will convert it to string
    value = eval(value)  
    *key, category = key.split(":") # as the dict contains key and value (category)
    # first question , topics of every subreddit
    if category  =="topics":
      #check first if the topic is none
        if topic is None:
            topic=key
        # if not , then count the most common discussed topics
        if topic != key:
            print(f"{topic}:{category}", count.most_common(10), sep='\t') # top three discussed topics
            topic = key
            count = Counter()
        count[value[0]] += value[1]
    # third question , highest upvotes
    if category  =="upvotes":
      if word_upvotes is None:
        word_upvotes = key
      if word_upvotes != key:
        if word_counting > 500: ## we take 120 , as an average number , because we notice that many numbers and we want the highest upvotes
          print(f"{word_upvotes}:{category}", count_upvotes, sep='\t')
          word_upvotes = key
          count_upvotes = 0
          word_counting = 0
      count_upvotes += value[0]
      word_counting += 1
# print the top three discussed topics
if category == "topics" and topic:
    print(f"{topic}:{category}", count.most_common(10), sep='\t') 
# print upvotes of the topics
if category == "upvotes" and word_upvotes:
  if word_counting > 500:
    print(f"{word_upvotes}:{category}", count_upvotes, sep='\t')

