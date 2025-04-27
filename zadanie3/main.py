import heapq

def create_dictionary(text):
    dictionary = {}
    for sign in text:
        dictionary[sign]+=1