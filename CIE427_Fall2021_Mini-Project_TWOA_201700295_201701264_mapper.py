#!/usr/bin/python3

import sys
import re
import os
import json
import spacy
from nltk.corpus import wordnet as wn
sys.path.insert(0, 'nltk')
import nltk
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
nltk.data.path.insert(0, "nltk_data")
# english stop word initalization
English_stopwords = nltk.corpus.stopwords.words('english')
#prepare the stemmer
stemmer = nltk.stem.porter.PorterStemmer() 
##here we initalize nouns to check noun
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')} 
for line in sys.stdin:
    #read as dict
    json_obj = json.loads(line)
    # take only subreddit
    subreddit_feature = json_obj["subreddit"]
    # take only body
    body_feature = json_obj["body"]
    #preprocessing starts
    # lower the body
    lowered_body = body_feature.lower() 
    non_alphanumeric_body = re.sub(r'[^\w ]+', '', lowered_body) # substitte in thing that is not charachter or number with nothing 
    no_links_body = re.sub(r'https?:\/\/.*[\r\n]*', '', non_alphanumeric_body) # i noticed that there is links in bdoy i talked this expression from here : https://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python/49257661
    # we will tokenize body to extract topics
    tokenization_of_body = nltk.tokenize.word_tokenize(no_links_body)
    for word in tokenization_of_body:
        ##check if the word is not stop word or numberic
        if word not in English_stopwords and len(word) <15 and not word.isnumeric() and word in nouns: # probably not a natural word 
          stemmed_word = stemmer.stem(word)
          ## print the subreddit and its topics
          print(f"{subreddit_feature}:topics", (stemmed_word, 1), sep='\t')
          ## print the topics and its upvotes
          print(f"{stemmed_word}:upvotes", (json_obj["ups"],), sep='\t')