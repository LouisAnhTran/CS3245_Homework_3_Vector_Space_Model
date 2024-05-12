#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import os
from nltk.stem.porter import *
from nltk.corpus import stopwords
from collections import defaultdict
import pickle
import math
from nltk.tokenize import RegexpTokenizer

import config
from Dictionary import Dictionary
from PostingList import PostingsList

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    # This is an empty method
    # Pls implement your code in below

    # get the list of all documents
    list_of_files=sorted(list(map(lambda x: int(x),os.listdir(in_dir)[:len(os.listdir(in_dir)) if not config.TESTING else config.TESTING_SIZE])))

    dictionary=dict()

    # get the set all stop words
    stop_words=set(stopwords.words('english'))

    number_of_documents=0

    dictionary_length_n=dict()

    for docid in list_of_files:
        with open(os.path.join(in_dir, str(docid)), "r") as file:
            dict_terms=dict()
            number_of_documents+=1 # increment the number of doc being indexed by 1 
            content=file.read()

            # tokenize the document content using sentence tokenization and word tokenization
            tokens=[token for sent in nltk.sent_tokenize(content) for token in nltk.word_tokenize(sent)] 

            # remove all stop words from the list of tokens
            tokens_with_no_stop_words=[token for token in tokens if token.lower() not in stop_words]
            tokens_with_no_stop_words=tokens

            # apply stemming and case folding
            stemmer = PorterStemmer()
            stemmed_and_case_folded_tokens=[stemmer.stem(token).lower() for token in tokens_with_no_stop_words]

            # iterate through all tokens of given doc and update the dictionary accordingly
            for token in stemmed_and_case_folded_tokens:
                if token not in dictionary:
                    dictionary[token]={docid:1}
                else:
                    dictionary[token][docid]=dictionary[token].get(docid,0)+1
                
                # increment the term frequency for given doc, will be used to compute doc length
                dict_terms[token]=dict_terms.get(token,0)+1
            
            
            if dict_terms:
                compute_document_length(dict_terms,docid,dictionary_length_n) # compute the doc length
            
    
    # modify the dictionary with posting list being sorted in order of increasing docid
    dictionary={term:sorted([(doc_id,term_freq) for doc_id,term_freq in dict_doc.items()]) for term,dict_doc in dictionary.items()}
    # save dictionary and posting to disks 
    dictionary_object=Dictionary(out_dict)
    posting_object=PostingsList(out_postings)
    posting_object.save_posting_to_disk(dictionary,dictionary_object)
    dictionary_object.save_dictionary_to_file()
    # save documents length to disk
    load_number_of_documents_to_disk(config.STORE_NUMBER_DOCS,number_of_documents)
    load_length_documents_to_disk(config.STORE_LENGTH_DOCS,dictionary_length_n)

def load_number_of_documents_to_disk(file_name,number_of_document):
    """
        write out the number of documents within the collection to hard disk
    """
    with open(file_name,'wb') as file:
        pickle.dump(number_of_document,file)

def load_length_documents_to_disk(file_name,length_N_dict):
    """
        write out the length of all documents to hard disk
    """
    with open(file_name,'wb') as file:
        pickle.dump(length_N_dict,file)

def compute_document_length(term_dict: dict,docid,length_d):
    """
        compute the lenght for given document
    """
    length_d[docid]=math.sqrt(sum([(1+math.log(val,10))**2 for val in term_dict.values()]))
    return length_d[docid]

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)
