#Name: Shrabya Timsina & Steven Cooklev
# CS121: Analyzing Election Tweets
# Part 2

import argparse
import json
import string
import sys
from util import sort_count_pairs, grab_year_month, pretty_print_by_month
from basic_algorithms import find_top_k, find_min_count, find_frequent

##################### DO NOT MODIFY THIS CODE ##################### 

PUNCTUATION = '!"$%\'()*+,-./:;<=>?[\\]^_`{|}~' + u"\u2014" + u"\u2026"

STOP_WORDS_SHORT = set(["a", "an", "the", "this", "that", "of", "for", "or", "and", "on", "to", "be", "if", "we", "you", "in", "is", "at", "it", "rt", "mt"])

STOP_WORDS = {"basic":STOP_WORDS_SHORT,
              "hrc":set(["clinton", "hillary", "tim", "timothy", "kaine"]).union(STOP_WORDS_SHORT),
              "djt": set(["donald", "trump", "mike", "michael", "pence"]).union(STOP_WORDS_SHORT),
              "both": STOP_WORDS_SHORT.union(set(["clinton", "hillary", "donald", "trump", "tim", "timothy", "kaine", "mike", "michael", "pence"])),
              "none": set([])}

STOP_PREFIXES  = {"default": set(["@", "#", "http", "&amp"]),
                  "hashtags_only": set(["#"]),
                  "none": set([])}

HRC_STOP_WORDS = STOP_WORDS["hrc"]
DT_STOP_WORDS = STOP_WORDS["djt"]
BOTH_CAND_STOP_WORDS = STOP_WORDS["both"]

# Tweets are represented as dictionaries that has the same keys and
# values as the JSON returned by twitter's search interface.

#####################  MODIFY THIS CODE ##################### 


# Task 1

def gener_value_list(tweets, entity_key, value_key):
    
    value_list = []

    for tweet in tweets:
        for entity in tweet["entities"][entity_key]:

            if tweet["entities"][entity_key] != None:
            
                lowering_case = entity[value_key].lower()
                value_list.append(lowering_case)

    return value_list

def find_top_k_entities(tweets, entity_key, value_key, k):
    '''
    Find the K most frequently occuring entitites

    Inputs:
        tweets: a list of tweets
        entity_key: a string ("hashtags", "user_mentions", etc)
        value_key: string (appropriate value depends on the entity type)
        k: integer 

    Returns: list of entity, count pairs sorted in non-decreasing order by count.

    '''
    
    val_list = gener_value_list(tweets, entity_key, value_key)
    top_k_entities = find_top_k(val_list, k) 


    return top_k_entities


# Task 2
def find_min_count_entities(tweets, entity_key, value_key, min_count):
    '''
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_key: a string ("hashtags", "user_mentions", etc)
        value_key: string (appropriate value depends on the entity type)
        min_count: integer 

    Returns: list of entity, count pairs sorted in non-decreasing order by count.
    '''

    val_list = gener_value_list(tweets, entity_key, value_key)
    mincount_entities = find_min_count(val_list, min_count)

    return mincount_entities

# Task 3
def find_frequent_entities(tweets, entity_key, value_key, k):
    '''
    Find entities where the number of times the specific entity occurs
    is at least fraction * the number of entities in across the tweets.

    Input: 
        tweets: a list of tweets
        entity_key: a string ("hashtags", "user_mentions", etc)
        value_key: string (appropriate value depends on the entity type)
        k: integer

    Returns: list of entity, count pairs sorted in non-decreasing order by count.
    '''
    
    val_list = gener_value_list(tweets, entity_key, value_key)
    freq_entities = find_frequent(val_list, k)
    

    return freq_entities


# Task 4

def preprocess(tweet_text, prefix_tuple, stop_words):
    
    lowercase_text = tweet_text.lower()
    split_text = lowercase_text.split()
            
            
    format_text = [] #list to store words after processing


    for word in split_text:
        word2 = word.strip(PUNCTUATION)
        if word2 not in stop_words and word2.startswith(prefix_tuple) == False and word2 != "":
            format_text.append(word2)

    return format_text


def gen_ngramslist(tweets, n, stop_words, stop_prefixes):

    prefix_tuple = tuple(stop_prefixes)

    value_list = []

    for tweet in tweets:
        if tweet["text"] != None: 

            format_text = preprocess(tweet["text"], prefix_tuple, stop_words)

            for index in range(0, len(format_text) - n + 1):
                    
                tuple_set = ()
                for i in range(0,n):
                         
                    tuple_set = tuple_set + (format_text[index + i],) 
                     
                value_list.append(tuple_set)

    return value_list

def find_top_k_ngrams(tweets, n, stop_words, stop_prefixes, k):
    '''
    Find k most frequently occurring n-grams or
    if k < 0, count occurrences of all n-grams
    
    Inputs:
        tweets: a list of tweets
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        k: integer

    Returns: list of key/value pairs sorted in non-increasing order
      by value.
    '''
    
    ngram_list = gen_ngramslist(tweets, n, stop_words, stop_prefixes)

    
    if k >= 0:
        topk_tuples = find_top_k(ngram_list, k)
       
    else:
        topk_tuples = find_top_k(ngram_list, len(ngram_list))



    return topk_tuples


# Task 5
def find_min_count_ngrams(tweets, n, stop_words, stop_prefixes, min_count):
    '''
    Find n-grams that occur at least min_count times.
    
    Inputs:
        tweets: a list of tweets
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        min_count: integer


    Returns: list of key/value pairs sorted in non-increasing order
      by value.
    '''
    ngram_list = gen_ngramslist(tweets, n, stop_words, stop_prefixes)
    mincount_ngram = find_min_count(ngram_list, min_count)

    return mincount_ngram


# Task 6
def find_frequent_ngrams(tweets, n, stop_words, stop_prefixes, k):
    '''
    Find frequently occurring n-grams

    Inputs:
        tweets: a list of tweets
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        k: integer

    Returns: list of key/value pairs sorted in non-increasing order
      by value.
    '''

    ngram_list = gen_ngramslist(tweets, n, stop_words, stop_prefixes)
   
    freq_ngram = find_frequent(ngram_list, k)

    if k >= 0:
        freq_ngram = find_frequent(ngram_list, k)
        
    else:
        freq_ngram = find_frequent(ngram_list, len(ngram_list))
    

    return freq_ngram


# Task 7

def find_top_k_ngrams_by_month(tweets, n, stop_words, stop_prefixes, k):
    '''                                                                                                            
    Find the top k ngrams for each month.

    Inputs:
        tweets: list of tweet dictionaries
        n: integer
        stop_words: a set of strings to ignore
        stop_prefixes: a set of strings.  Words w/ a prefix that
          appears in this list should be ignored.
        k: integer

    Returns: sorted list of pairs.  Each pair has the form: 
        ((year,  month), (sorted top-k n-grams for that month with their counts))
    '''
    
    prefix_tuple = tuple(stop_prefixes)


    tweet_month_dic = {}

    for tweet in tweets:
        year_month = grab_year_month(tweet["created_at"])
        tweet_month_dic[year_month] = tweet_month_dic.get(year_month, [])


        if tweet["text"] != None: 

            format_text = preprocess(tweet["text"], prefix_tuple, stop_words)


            for index in range(0, len(format_text) - n + 1):
                #tuple_elements = []
                tuple_set = ()
                for i in range(0,n):
                    #tuple_elements.append(format_text[index + i]) 
                    tuple_set = tuple_set + (format_text[index + i],) 
                 
                #value_list.append(tuple(tuple_elements))
                tweet_month_dic[year_month].append(tuple_set)


    
    topk_tweet_month = []
    for month, n_gram in tweet_month_dic.items():
        top_k_ngrams = find_top_k(n_gram, k)
        pass_value = (month, top_k_ngrams)
        topk_tweet_month.append(pass_value)


    ordered_topk = sorted(topk_tweet_month)




        

    return ordered_topk

    





def parse_args(args):
    '''                                                                                                                
    Parse the arguments                                                                                                
    '''
    parser = argparse.ArgumentParser(description='Analyze presidential candidate tweets .')
    parser.add_argument('-t', '--task', nargs=1, help="<task number>", type=int, default=[0])
    parser.add_argument('-k', '--k', nargs=1, help="value for k", type=int, default=[1])
    parser.add_argument('-c', '--min_count', nargs=1, help="min count value", type=int, default=[1])
    parser.add_argument('-n', '--n', nargs=1, help="number of words in an n-gram", type=int, default=[1])
    parser.add_argument('-e', '--entity_key', nargs=1, help="entity key for task 1", type=str, default=["hashtags"])
    parser.add_argument('file', nargs=1, help='name of JSON file with tweets')

    try:
        return parser.parse_args(args[1:])
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

def go(args):
    task = args.task
    
    task = task[0]

    if task <= 0 or task > 7:
        print("The task number needs to be a value between 1 and 7 inclusive.",
              file=sys.stderr)
        sys.exit(1)
        
    ek2vk = {"hashtags":"text", 
             "urls":"url", 
             "user_mentions":"screen_name"}

    if task in [1,2,3]:
        ek = args.entity_key=args.entity_key[0]
        if ek not in ek2vk:
            print("Entity type must be one of: hashtags, urls, or user_mentions", 
                  file=sys.stderr)
            sys.exit(1)
        else:
            vk = ek2vk[ek]

    try:
        tweets = json.load(open(args.file[0]))
    except OSError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if task == 1:
        print(find_top_k_entities(tweets, ek, vk, args.k[0]))

    elif task == 2:
        print(find_min_count_entities(tweets, ek, vk, args.min_count[0]))

    elif task == 3:
        print(find_frequent_entities(tweets, ek, vk, args.k[0]))

    elif task == 4:
        print(find_top_k_ngrams(tweets, args.n[0], BOTH_CAND_STOP_WORDS, 
                                STOP_PREFIXES["default"], args.k[0]))
    elif task == 5:
        print(find_min_count_ngrams(tweets, args.n[0], BOTH_CAND_STOP_WORDS, 
                                    STOP_PREFIXES["default"], args.min_count[0]))
    elif task == 6:
        print(find_frequent_ngrams(tweets, args.n[0], BOTH_CAND_STOP_WORDS, 
                                   STOP_PREFIXES["default"], args.k[0]))
    elif task == 7:
        result = find_top_k_ngrams_by_month(tweets, args.n[0], BOTH_CAND_STOP_WORDS, 
                                            STOP_PREFIXES["default"], args.k[0])
        pretty_print_by_month(result)



if __name__=="__main__":
    args = parse_args(sys.argv)
    go(args)



