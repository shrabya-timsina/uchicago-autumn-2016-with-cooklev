# Name: Shrabya Timsina & Steven Cooklev
# CS121: Analyzing Election Tweets
# Part 1

from util import sort_count_pairs


def find_top_k(items, k):
    '''
    Find the k most frequently occuring items

    Inputs:
        items: a list of items
        k: integer 

    Returns: sorted list of K tuples
    '''
    
    dic_itemcount = {}

    # getting count of items
    for item in items:
        dic_itemcount[item] = dic_itemcount.get(item, 0) + 1

    # make the dictionary into a list
    list_itemcount = dic_itemcount.items()

    # use the given sort function and splice first k elements
    ordered_itemcount = sort_count_pairs(list_itemcount)
    first_k_items = ordered_itemcount[0:k] 

    return first_k_items


def find_min_count(items, min_count):
    '''
    Find the items that occur at least min_count times

    Inputs:
        items: a list of items    
        min)count: integer
        
    Returns: sorted list of tuples
    '''

    dic_allcount = {}

    # getting count of items
    for item in items:
        dic_allcount[item] = dic_allcount.get(item, 0) + 1

    list_mincount = [(item, count) for item, count in dic_allcount.items() if count >= min_count]

    # use the given sort function
    ordered_mincount = sort_count_pairs(list_mincount)
    
    return ordered_mincount


def find_frequent(items, k):
    '''
    Find items where the number of times the item occurs is at least
    fraction * len(items).

    Input: 
        items: list of items
        k: integer

    Returns: sorted list of tuples
    '''

    freq_dic = {}
    
    # use if and else statements to implement the bullet-point
    # instructions within the for loop
    for item in items:
        if item not in freq_dic:
            if len(freq_dic) < (k - 1):
                freq_dic.update({item: 1})
            else:
                freq_dic = {item: count - 1 for item, count in freq_dic.items()}
                freq_dic = {item: count for item, count in freq_dic.items() if count != 0}
        else: 
            freq_dic[item] = freq_dic[item] + 1
    ordered_freq_list = sort_count_pairs(freq_dic.items())

    return ordered_freq_list