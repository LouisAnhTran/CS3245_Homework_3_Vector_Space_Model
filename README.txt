This is the README file for A0290532J's submission
Email(s): e1325138@u.nus.edu

== Python Version ==

I'm using Python Version <3.10.7> for this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps in your program, and discuss your experiments in general.  A few paragraphs are usually sufficient.

The entire program is composed of two main parts, namely indexing and seaching and each part contain various helper functions to implement required algorithms and logics. In this section, i will provide detailed used algorithms and steps for both parts

I. Indexing:

The purpose of indexing is to create a dictionary of all terms within collection which contains correct pointers pointing to pointing lists stored in the hard disk.

Hence, the expected dictionary and posting list should have the following structure:

Dictionary: 

{term:(document_frequency,pointer_to_poiting_list),...}

Posting List for a specific:

[(doc_id_1,term_frequency_1),(doc_id_2,term_frequency_2),....(doc_id_n,term_frequency_n)] => sorted in ascending order of doc_id

1. Tokenization, Stemming, Stop Word Removal:
   - Retrieve all docids from the Reuters corpus data.
   - Initialize a variable for the dictionary of terms, denoted as D.
   - Initialize a variable to keep track of the length for documents, denoted as D1.
   - Initialize a variable to keep track of total documents, denoted as N.
   - Iterate through each docid and open the corresponding document. For each document, perform the following steps:
     + Increment N by 1.
     + Initialize a dictionary to keep track of occurrences for each term in the document, denoted as D2, which will be used to calculate the length for the document vector.
     + Obtain the list of tokens using `sent_tokenize` and `word_tokenize` provided by NLTK.
     + Retrieve the list of stop words from NLTK.
     + Create a new list of tokens using list comprehension and applying these conditions: a token must not be in the stop word list, apply stemming, and case-folding to reduce the token to its lowercase form.
     + Once a list of tokens is obtained in accordance with the requirements, iterate through each token. For each token, perform the following steps:
       - If the token is not in the dictionary, add this token to dictionary D as a key, with the value being {docid: 1}.
       - Otherwise, update the term frequency of this term for the given docid.
       - Update the term frequency in the current docid in D2.
     + Compute the document length d and add the docid to D1 as a key and its corresponding value for document length as d.
   - Update D by implementing sorting for the posting list by docid in dictionary D.

2. Writing out Dictionary and Posting Lists to Hard Disk:
   - Instantiate a dictionary object from the Dictionary class.
   - Instantiate a posting list object from the PostingList class.
   Notice: The dictionary to be loaded into memory for searching will look like: `{docid: (document_frequency, offset or pointer)}`, where the offset is the pointer to the corresponding posting list on the hard disk.
   - Iterate through all terms in dictionary D from part 1. For each term:
     + Get the current pointer on the hard disk.
     + Retrieve the posting list from the dictionary D.
     + Convert the posting list to a linked list with skip pointers.
     + Add the term to the dictionary as the key, with values being a tuple containing document frequency and a pointer to the posting list.
     + Write out the pointing list to the hard disk.
   - At this point, we have successfully constructed the dictionary, with each term having a pointer to its respective posting list on the hard disk. Then, write out the term dictionary, document length dictionary as well as the number of documents to the hard disk to complete the indexing phase.

II. Searching:

For each query from the given query file, we will perform the following steps:

1. Tokenizing and Sanitizing the Query:
   - Tokenize the given query.
   - For each term in the query, remove leading and trailing punctuation such as commas and periods.
   - Return a tokenized and sanitized query.

2. Convert Query to Vector:
   - Create a dictionary from the query with keys being the terms and values being their occurrences in the query.
   - Read the number of documents from the memory, denoted as N.
   - Iterate through every key in the dictionary and update its corresponding value using the given formula: (1+log(tf))*log(N/df)
   - Return a query vector.

3. Calculating the Score:
   - Initialize the dictionary to store documents and their corresponding scores.
   - Iterate through each term in the query.
   - For each term, do the following steps:
     - Load the posting list from memory using the offset.
     - Iterate through every document in the posting list. For each document, do the following steps:
       - Update the document score in the dictionary using the given formula: {dictionary}[doc_id] = w(t,d)*w(t,q), where w(t,d) = 1+log({term\_frequency}) and w(t,q) is the value of the key term from the query vector.
   - After the for loop terminates, we get the dictionary keeping track of unnormalized scores for all documents.
   - To do normalization, we load the document length created during the indexing phase from memory. We take the unnormalized score of the document ID and divide it by the corresponding document length to obtain the normalized score.
   - At this stage, we successfully calculate the normalized score for all document IDs for the given query.

4. Return the Top 10 Documents with the Highest Score:
   - The algorithm for this is straightforward, and the steps are explained properly in the `search.py` file.
   - The detail will not be covered here because it is not part of the requirements.
   - If two documents have the same score, the document with the smaller ID will be ranked higher in the output result.


== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

In order to implement Indexing and Searching tasks, I have created a couple of files for storing intermediarty data.

index.py: Contains logic for carrying out the indexing task.
search.py: Contains logic for performing searches on text queries.
dictionary.txt: A file to store the dictionary on the hard disk.
postings.txt: A file to store posting lists on the hard disk.
number_of_documents.txt: Stores the number of documents in the collection after the indexing phase for idf calculation.
length_documents.txt: Stores the dictionary with the key being the document ID and the value being the corresponding length of the document vector.
Dictionary.py: A class defined to manage dictionary operations, storage, writing to the hard disk, and loading from the hard disk to memory for searching.
PostingList.py: A class defined to manage PostingList objects in a standardized and organized manner for operations such as writing out posting lists to the hard disk, and reading in a posting list for a specific term from the hard disk to memory for searching.
README.txt: Provides additional information about the assignment, such as algorithm and steps elaboration, submitted files, student declaration, references, etc.

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I/We, A0290532J, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0290532J, did not follow the class rules regarding homework
assignment, because of the following reason:

I adhered strictly to the course policy, assignment guidelines, and class rules in order to complete this assignment.

We suggest that we should be graded as follows:

Code correctness, readability, and scalability
Adherence to submission instructions and guidelines
Accurate application and implementation of concepts and algorithms covered in lectures.

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

Learning pickle: 
1. https://docs.python.org/3.7/library/pickle.html

