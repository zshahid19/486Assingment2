#!/usr/bin/env python3
#zshahid
import sys
import re
import os
import math
from PorterStemmer import PorterStemmer



#Input: A string containing the text from a file
#Output: the string with all the SGML tags removed
#Purpose: remove all the SGML tags from the input string
def removeSGML(file_text):
    #removed all SGML tags
    clean_text = re.sub(r'<.*?>', '', file_text)
    # print(clean_text)
    return clean_text


#Input: Take in cleaned text (no SGML text)
#Output: List (of tokens)
#Purpose: Take in the cleaned text, tokenize that text then return list of tokens of that text
def tokenizeText(cleaned_text):
    # Expand contractions
    def expand_contractions(token):
        contractions = { "I'm": "I am", "I'm'a": "I am about to", "I'm'o": "I am going to", "I've": "I have", "I'll": "I will", "I'll've": "I will have", "I'd": "I would", "I'd've": "I would have", "Whatcha": "What are you", "amn't": "am not", "ain't": "are not", "aren't": "are not", "'cause": "because", "can't": "cannot", "can't've": "cannot have", "could've": "could have", "couldn't": "could not", "couldn't've": "could not have", "daren't": "dare not", "daresn't": "dare not", "dasn't": "dare not", "didn't": "did not", "didn’t": "did not", "don't": "do not", "don’t": "do not", "doesn't": "does not", "e'er": "ever", "everyone's": "everyone is", "finna": "fixing to", "gimme": "give me", "gon't": "go not", "gonna": "going to", "gotta": "got to", "hadn't": "had not", "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not", "he've": "he have", "he's": "he is", "he'll": "he will", "he'll've": "he will have", "he'd": "he would", "he'd've": "he would have", "here's": "here is", "how're": "how are", "how'd": "how did", "how'd'y": "how do you", "how's": "how is", "how'll": "how will", "isn't": "is not", "it's": "it is", "'tis": "it is", "'twas": "it was", "it'll": "it will", "it'll've": "it will have", "it'd": "it would", "it'd've": "it would have", "kinda": "kind of", "let's": "let us", "luv": "love", "ma'am": "madam", "may've": "may have", "mayn't": "may not", "might've": "might have", "mightn't": "might not", "mightn't've": "might not have", "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have", "ne'er": "never", "o'": "of", "o'clock": "of the clock", "ol'": "old", "oughtn't": "ought not", "oughtn't've": "ought not have", "o'er": "over", "shan't": "shall not", "sha'n't": "shall not", "shalln't": "shall not", "shan't've": "shall not have", "she's": "she is", "she'll": "she will", "she'd": "she would", "she'd've": "she would have", "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have", "so's": "so is", "somebody's": "somebody is", "someone's": "someone is", "something's": "something is", "sux": "sucks", "that're": "that are", "that's": "that is", "that'll": "that will", "that'd": "that would", "that'd've": "that would have", "'em": "them", "there're": "there are", "there's": "there is", "there'll": "there will", "there'd": "there would", "there'd've": "there would have", "these're": "these are", "they're": "they are", "they've": "they have", "they'll": "they will", "they'll've": "they will have", "they'd": "they would", "they'd've": "they would have", "this's": "this is", "this'll": "this will", "this'd": "this would", "those're": "those are", "to've": "to have", "wanna": "want to", "wasn't": "was not", "we're": "we are", "we've": "we have", "we'll": "we will", "we'll've": "we will have", "we'd": "we would", "we'd've": "we would have", "weren't": "were not", "what're": "what are", "what'd": "what did", "what've": "what have", "what's": "what is", "what'll": "what will", "what'll've": "what will have", "when've": "when have", "when's": "when is", "where're": "where are", "where'd": "where did", "where've": "where have", "where's": "where is", "which's": "which is", "who're": "who are", "who've": "who have", "who's": "who is", "who'll": "who will", "who'll've": "who will have", "who'd": "who would", "who'd've": "who would have", "why're": "why are", "why'd": "why did", "why've": "why have", "why's": "why is", "will've": "will have", "won't": "will not", "won't've": "will not have", "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all", "y'all're": "you all are", "y'all've": "you all have", "y'all'd": "you all would", "y'all'd've": "you all would have", "you're": "you are", "you've": "you have", "you'll've": "you shall have", "you'll": "you will", "you'd": "you would", "you'd've": "you would have", "to cause": "to cause", "will cause": "will cause", "should cause": "should cause", "would cause": "would cause", "can cause": "can cause", "could cause": "could cause", "must cause": "must cause", "might cause": "might cause", "shall cause": "shall cause", "may cause": "may cause" }
        return contractions.get(token, [token])

    # get the whole date   
    def is_date(char, current_token):
        return char in ['/', '-'] and any(c.isdigit() for c in current_token)
    
    # get the whole acronym
    def is_acronym(i, char, text):
        return char == '.' and i < len(text) - 1 and text[i + 1].isupper()
    
    #  checking for big number digits or commas
    def is_big_number(char, current_token):
        return char.isdigit() or (char == ',' and current_token and current_token.replace(',', '').isdigit())

    tokens = []
    current_token = ''
    word_start = True  # Flag to indicate start of a new word

    for i, char in enumerate(cleaned_text):
        if char.isspace() or char in '.!?':
            word_start = True
            if current_token:
                tokens.extend(expand_contractions(current_token))
                current_token = ''
            continue

        if word_start and current_token:
            # If we are at a word start, finalize the previous token
            tokens.extend(expand_contractions(current_token))
            current_token = ''
        
        word_start = False  # Reset word start flag as we are in the middle of a word

        # logic for handling character addition to tokens
        if (char.isalpha() or char in ['\'', '-'] or 
            is_date(char, current_token) or 
            is_big_number(char, current_token)):
            current_token += char
        elif char == '.' and (is_big_number(char, current_token) or is_acronym(i, char, cleaned_text)):
            current_token += char
        else:
            if current_token:
                tokens.extend(expand_contractions(current_token))
                current_token = ''

        # Handle the final token
    if current_token:
            tokens.extend(expand_contractions(current_token))

    return tokens



def indexDocument(doc_id, doc_content, doc_weighting_scheme, inverted_index, doc_lengths):
    # Preprocess the content
    cleaned_content = removeSGML(doc_content)
    tokens = tokenizeText(cleaned_content)
    # print(tokens)

    # stemming  using porterstemmer
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token, 0, len(token) - 1) for token in tokens]

    # adding tokens to the inverted index and counts for term weights
    for token in stemmed_tokens:
        if token not in inverted_index:
            inverted_index[token] = {}
        if doc_id not in inverted_index[token]:
            inverted_index[token][doc_id] = 0
        inverted_index[token][doc_id] += 1

    # Calculating term weights for the document
    if doc_weighting_scheme == "tfc":
        for token in stemmed_tokens:
            tf = inverted_index[token][doc_id]
            idf = math.log((len(doc_lengths) + 1) / (len(inverted_index[token]) + 1))
            inverted_index[token][doc_id] = tf * idf
    elif doc_weighting_scheme == "nfx":
        max_tf = max(inverted_index[token][doc_id] for token in stemmed_tokens)
        for token in stemmed_tokens:
            tf = inverted_index[token][doc_id] / max_tf
            idf = math.log((len(doc_lengths) + 1) / (len(inverted_index[token]) + 1))
            inverted_index[token][doc_id] = tf * idf

    # Update document length for nomilization
    doc_length = sum([inverted_index[token][doc_id]**2 for token in stemmed_tokens])
    doc_lengths[doc_id] = math.sqrt(doc_length)


def retrieveDocuments(query, inverted_index, query_weighting_scheme, doc_lengths):
    # Preprocess the query
    cleaned_query = removeSGML(query)
    query_tokens = tokenizeText(cleaned_query)

    # Apply stemming to the query tokens
    stemmer = PorterStemmer()
    stemmed_query_tokens = [stemmer.stem(token, 0, len(token) - 1) for token in query_tokens]

    # Calculate term frequency for each term in the query
    query_term_freq = {}
    for token in stemmed_query_tokens:
        if token not in query_term_freq:
            query_term_freq[token] = 0
        query_term_freq[token] += 1

    # Determine the set of documents that include at least one token from the query
    relevant_docs = set()
    for token in stemmed_query_tokens:
        if token in inverted_index:
            relevant_docs.update(inverted_index[token].keys())

    #calculate similarity scores between the query and each relevant document
    similarity_scores = {}
    for doc_id in relevant_docs:
        score = 0
        for token in stemmed_query_tokens:
            if token in inverted_index and doc_id in inverted_index[token]:
                # Calculate term weights for the query and document
                doc_term_weight = inverted_index[token][doc_id]
                if query_weighting_scheme == "tfx":
                    query_term_weight = query_term_freq[token] 
                elif query_weighting_scheme == "bpx":
                    query_term_weight = 0
                    if token in query_tokens:
                        n = len(inverted_index[token])
                        idf = math.log((len(doc_lengths) + 1) / (n + 1))
                        # idf = math.log((len(doc_lengths) + 1) / (n))
                        query_term_weight = idf
                else:
                    query_term_weight = 0

                score += doc_term_weight * query_term_weight

        # Normalize the score by the document length
        if doc_lengths[doc_id] != 0:
            score /= doc_lengths[doc_id]
        similarity_scores[doc_id] = score

    return similarity_scores




def main():
    if len(sys.argv) < 5:
        print("Usage: vectorspace.py <document_weighting(tfc/nfx)> <query_weighting(tfx/bpx)> <doc_collection_folder> <query_file>")
        sys.exit(1)

    doc_weighting = sys.argv[1]
    query_weighting = sys.argv[2]
    doc_collection_folder = sys.argv[3]
    query_file = sys.argv[4]

    inverted_index = {}
    doc_lengths = {}

    # Index each document in the collection
    for filename in os.listdir(doc_collection_folder):
        filepath = os.path.join(doc_collection_folder, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                content = file.read()
                indexDocument(filename, content, doc_weighting, inverted_index, doc_lengths)

    output_filename = f"cranfield.{doc_weighting}.{query_weighting}.output"

    # write in output file
    with open(output_filename, 'w') as output:
        with open(query_file, 'r') as file:
            query_id = 1
            for query in file.readlines():
                similarity_scores = retrieveDocuments(query, inverted_index, query_weighting, doc_lengths)
                #sort documents by similarity score in DESECENDING order
                sorted_scores = sorted(similarity_scores.items(), key=lambda item: item[1], reverse=True)
                for doc_id, score in sorted_scores:
                    output.write(f"{query_id} {doc_id} {score:.2f}\n")
                query_id += 1

if __name__ == "__main__":
    main()

