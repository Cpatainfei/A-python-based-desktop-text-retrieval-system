from xml.dom.minidom import parse
from collections import Counter
import math
import json
import numpy as np
import os
import re


# Read out files from the dataset 

# Retain document texts and document id

document_path = './CA6005_2022/COLLECTION/COLLECTION/'
document_list = os.listdir(document_path)              # All the documents files
Documents_id = []                                      # Document IDs
Documents = []                                         # Documents List


for i in document_list:
    filename = document_path + i
    document_tree = parse(filename)
    content = document_tree.documentElement
    text = content.getElementsByTagName('TEXT')
    text = text[0].firstChild
    
    # Drop out one document whose text is empty
    if type(text) == type(None):
        continue
    else:
        text = text.data
    DOCID = content.getElementsByTagName('DOCID')
    DocID = DOCID[0].firstChild.data
    Documents.append(text)
    Documents_id.append(DocID)

    
# Same operation for query


query_path = './CA6005_2022/topics/topics/'
query_list = os.listdir(query_path)
Query_id = []
Query = []

for i in query_list:
    filename = query_path + i
    query_tree = parse(filename)
    content = query_tree.documentElement
    text = content.getElementsByTagName('TITLE')
    text = text[0].firstChild
    
    # One document has no text
    if type(text) == type(None):
        continue
    else:
        text = text.data
    QUERYID = content.getElementsByTagName('QUERYID')
    queryid = QUERYID[0].firstChild.data
    Query.append(text)
    Query_id.append(queryid)
    
    
    
    
# Vocabulary building and text preprocessing(note: This step may take some seconds and your memory in the machine to run)

vocabulary = []

# Define punctuation 

punctuation = list('!"#$%&()*+,\'-./:;<=>?@[\\]^_‘{|}~ ')

# Define stop words
stop_words = list('the who she and you not your but hime his will what her are our for was to in that is not with'.split())


for i in range(len(Documents)):
    d = Documents[i]
    # Normalization
    d = d.lower()
    
    # Tokenization
    lst_d = d.split(" ")
    
    fixed = []
    
    # remove all the punctuations, stop words and words whose length less that 2
    
    for j in lst_d:
        if j not in punctuation and j not in stop_words and len(j)>2:
            fixed.append(j)

    Documents[i] = fixed
    # Store words in the vocabulary
    for k in fixed:
        vocabulary.append(k)

# Same operation for querys

for i in range(len(Query)):
    q = Query[i]
    # Normalization
    q = q.lower()
    # Tokenization
    lst_q = q.split(" ")
    
    fixed = []
    
    for j in lst_q:
        if j not in punctuation and j not in stop_words and len(j)>2:
            fixed.append(j)
            
    Query[i] = fixed


        
#frequency = Counter(vocabulary)

#Build vocabulary
vocabulary = list(set(vocabulary))


# Put documents and query together in dictionaries(ID, Queries/Documents)

document_dic = dict(zip(Documents_id,Documents))
query_dic = dict(zip(Query_id,Query))


# Indexing, inverted index was used here

Inverted_index = {}

for doc in document_dic.items():
    words = set(doc[1])
    for word in words:
        if word in Inverted_index.keys():
            Inverted_index[word].append(doc[0])
        else:
            Inverted_index[word] = [doc[0]]
            

# Write vocabulary, queries, documents and index in files 

with open("documents","w") as file:
    file.write(json.dumps(document_dic))

with open("queries","w") as file:
    file.write(json.dumps(query_dic))

with open("Inverted_index","w") as file:
    file.write(json.dumps(Inverted_index))
    
with open("vocabulary", "w") as file:
    for i in vocabulary:
        file.write(i)
        file.write(" ")