#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import string 
import re
from nltk.stem.porter import *
from nltk.corpus import stopwords
import pickle
import math 
from nltk.tokenize import RegexpTokenizer


import config
from Dictionary import Dictionary
from PostingList import PostingsList

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    # This is an empty method
    # Pls implement your code in below
    
    # retrieve dictionary from memory
    dictionary_object=Dictionary(dict_file)
    dictionary=dictionary_object.load_dictionary_from_file()

    # instantiate posting list object
    posting_list=PostingsList(postings_file)

    # load number of documents from memory
    number_of_docs=load_data_from_memory(config.STORE_NUMBER_DOCS)

    # load dictionary of document length from memory
    length_dictionary=load_data_from_memory(config.STORE_LENGTH_DOCS)

    with open(results_file,'w') as out_file:
        with open(queries_file,'r') as queries_file:
            queries=queries_file.readlines()
            for query in queries:
                # convert query to vector
                query=query.strip()
                query_terms=tokenize_and_sanitize_query(query) # tokenize the query 
                vector_query=convert_query_to_vector(query_terms,dictionary,number_of_docs) # construct the vector query
                if vector_query:
                    score_dictionary=implement_cosine_score_for_a_query(vector_query,posting_list,length_dictionary,dictionary)
                    result=return_top_k_docs(score_dictionary)
                    out_file.write(result+"\n")
                else:
                    out_file.write(""+"\n")

def implement_cosine_score_for_a_query(vector_query,posting_lists:PostingsList,length_dictionary,dictionary):
    """
        implement the cosine score computation for a given query
    """
    score_dictionary={}
    for term in vector_query:
        # load the posting list given the term
        fetch_post_list=posting_lists.load_posting_from_disk(dictionary[term][1])
        for docid,tf in fetch_post_list: 
            score_dictionary[docid]=score_dictionary.get(docid,0)+(1+math.log(tf,10))*vector_query[term]
    # normalize the score
    score_dictionary={docid:(score_before_normalization/length_dictionary[docid]) for docid,score_before_normalization in score_dictionary.items()}
    return score_dictionary    

def return_top_k_docs(score_dictionary):
    """
        return a top documents with highest normalized scores
    """
    top_k=[]
    # if total number of documents fewer or equal top k doc, the output return all documents
    actual_rank=config.NUMBER_OF_RANKING if config.NUMBER_OF_RANKING<=len(score_dictionary.keys()) else len(score_dictionary.keys())
    while len(top_k)<actual_rank:
        max_value=max([val for key,val in score_dictionary.items() if key not in top_k])
        # if docs have the same score, sort the results in the order of increasing docid
        docs_match_max=sorted([key for key in score_dictionary if score_dictionary[key]==max_value])
        top_k.extend(docs_match_max if len(docs_match_max)<=(actual_rank-len(top_k)) else docs_match_max[:actual_rank-len(top_k)])
    return " ".join(list(map(str,top_k)))

def load_data_from_memory(filename):
    """
        load data structure or object from the hard disk
    """
    with open(filename,'rb') as file:
        return pickle.load(file)
    
def tokenize_and_sanitize_query(query_term):
    """
        tokenize the query using sentence tokenization, word tokenization, case folding and stemming
    """
    stop_words=set(stopwords.words('english'))
    tokens=[word for sentence in nltk.sent_tokenize(query_term) for word in nltk.word_tokenize(sentence)]
    tokens_without_stop_words=[token for token in tokens if token.lower not in stop_words]
    tokens_without_stop_words=tokens
    stemmer=PorterStemmer()
    query_terms=[stemmer.stem(token).lower() for token in tokens_without_stop_words] # stemming and lower case
    return query_terms

def remove_punctuation_token(token):
    punctuation_set = {",","."}
    i=0
    while i<len(token) and token[i] in punctuation_set:
        i+=1
    if i==len(token):
        return ""
    left_token=token[i:]
    i=len(left_token)-1
    while i>=0 and left_token[i] in punctuation_set:
        i-=1
    right_token=left_token[:i+1]
    return right_token


def convert_query_to_vector(query_terms,dictionary,number_of_docs):
    """
        convert the query into vector, using (1+log(tf))*(log(N/df)) formula
    """
    query_terms=[term for term in query_terms if term in dictionary] # remove term that not appear in dictionary or vocabulary
    if not query_terms:
        return None
    dict_query_terms=dict()
    for term in query_terms:
        dict_query_terms[term]=dict_query_terms.get(term,0)+1
    # apply the formula: (1+log(tf))*(log(N/df)) 
    vector_query={term:(1+math.log(tf,10))*math.log(number_of_docs/dictionary[term][0],10) for term,tf in dict_query_terms.items()}
    return vector_query


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
