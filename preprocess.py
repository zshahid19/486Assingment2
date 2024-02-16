#!/usr/bin/env python3
#zshahid
import os
import re
import sys
"""
Module Docstring
"""

# Questions:
# How should numbers, peroids be handled. Yes to them in abreviations or no spec is confusing
# What exactly should I be adding to my vocabulary just subwords?
# how to handle start before each word? just add a start before every token? or just assume in BPE? Or Start in just start of sentences??
# how am I to return merge rules? number of merge rules or strings of the rules?

#Input: folder_path (path towards the folder with the dataset)
#Output: List containing all the files from the input folder_path
#Purpose: to turn the folder_path and give the user an actual manipultable data
def list_files_in_folder(folder_path):
    #Empty file_path list
    file_paths = []
    
    if not os.path.isdir(folder_path):
        print(f"Path does not exist")
        return file_paths

    #Iterating thorugh folder
    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)
        # If good add it to the list
        if os.path.isfile(full_path):
            file_paths.append(full_path)

    return file_paths

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

    
#Input: tokenized_text list of pre-tokenized text (list of strings)
#Output: Set of unique characters in the tokenized text 
#Purpose: find the vocabulary from the tokenized text
def create_initial_vocabulary(tokens):
    vocabulary = {}
    for token in tokens:
        for character in token:
            vocabulary[character] = vocabulary.get(character, 0) + 1
    return vocabulary


#Input: tokenized_text
#Output: dict with pair frequencies
#Purpose: Calculates the frequinces of character pairs
def find_most_frequent_pair(merged_freqs):
    # Find the pair with the highest frequency
    if not merged_freqs:
        return None  # Return None if merged_freqs is empty
    return max(merged_freqs, key=merged_freqs.get)


#Input: our working_dict, current vocab dict
#Output: dictonary with potential merged tokens and their frequencies
#Purpose: calculate the frequencies of potential merged tokens based on working dictionary.
def calculate_merged_token_frequencies(working_dict, vocabulary):
    merged_freqs = {}
    for char_list, freq in working_dict.items():
        for i in range(len(char_list) - 1):
            # Ensure pairs are stored as tuples in merged_freqs
            pair = (char_list[i], char_list[i + 1])
            if pair not in vocabulary:  # Assuming vocabulary stores merged tokens as keys
                merged_freqs[pair] = merged_freqs.get(pair, 0) + freq
    return merged_freqs

def find_most_frequent_new_token(merged_freqs, vocabulary):
    for merged_token, freq in sorted(merged_freqs.items(), key=lambda x: x[1], reverse=True):
        if merged_token not in vocabulary:
            return merged_token
    return None


    #Input: vocab dictonary, string of new token, frequency of new token
    #Output: none!
    #Purpose: - update the frequency of the new merged token in the vocab list
    #         - Also decrement frequencies of the old tokens
def update_vocabulary_frequency(vocabulary, tokens_to_merge, new_token, frequency):
    # Example logic for decreasing frequency of original tokens
    for token in tokens_to_merge:
        if token in vocabulary:
            vocabulary[token] -= frequency
    # Add or update the new merged token
    vocabulary[new_token] = frequency



    #Input: our tokenized list
    #Output: working_dict (keys are tuples of characters from tokens, values are their frequencies)
    #Purpose: initialize a working dictionary from the list of tokens, breaking each token into individual characters and counting their frequencies.
    # we yse this dict to do our merging on 
def initialize_working_list(tokens):
    working_dict = {}
    for token in tokens:
        # Break down token into individual characters
        char_list = [char for char in token]
        working_dict[tuple(char_list)] = working_dict.get(tuple(char_list), 0) + 1
    return working_dict




#input: working dictonary, new merged token
#output: updated workign dictornary
#purpose: add the new merged token into the merged dictonary
def merge_in_working_list(working_dict, tokens_to_merge, new_merged_token):
    new_working_dict = {}
    for char_list, freq in working_dict.items():
        # Attempt to merge the specified tokens within each char_list
        new_char_list = []
        i = 0
        while i < len(char_list):
            # Check if the next tokens in the char_list match the tokens_to_merge
            if i < len(char_list) - len(tokens_to_merge) + 1 and all(char_list[i+j] == tokens_to_merge[j] for j in range(len(tokens_to_merge))):
                # If they match, replace them with the new_merged_token
                new_char_list.append(new_merged_token)
                i += len(tokens_to_merge)  # Skip past the merged tokens
            else:
                new_char_list.append(char_list[i])
                i += 1

        # Convert the new_char_list back to a tuple and update the frequency
        new_key = tuple(new_char_list)
        new_working_dict[new_key] = new_working_dict.get(new_key, 0) + freq

    return new_working_dict


    # Decrease the frequencies of the constituent tokens
    # for i in range(1, len(new_token)):
    #     part1 = new_token[:i]
    #     part2 = new_token[i:]
    #     if part1 in vocabulary:
    #         vocabulary[part1] -= frequency
    #     if part2 in vocabulary:
    #         vocabulary[part2] -= frequency


#inpit: token list, vocab size
#output: vocab list (should have size of vocab size), merge rules used
#purpose: the entire bpe function does bpe shit
def bpe(token_list, vocab_size):
    #flatten list
    tokens = [token for sublist in token_list for token in sublist]
    initial_vocabulary = create_initial_vocabulary(tokens)
    vocabulary = dict(initial_vocabulary)
    working_dict = initialize_working_list(tokens)
    merge_rules = []

    # Loop until the vocabulary size meets desired number
    while len(vocabulary) < vocab_size:
        merged_freqs = calculate_merged_token_frequencies(working_dict, vocabulary)
        most_frequent_pair = find_most_frequent_pair(merged_freqs)
        # print("Vocabulary size currently: ", len(vocabulary))
        tokens_to_merge = most_frequent_pair  # This should already be a tuple
        new_merged_token = ''.join(tokens_to_merge)
        frequency_of_new_token = merged_freqs[most_frequent_pair]
        # If no pair is found, exit the loop
        if not most_frequent_pair:
            break
        update_vocabulary_frequency(vocabulary, tokens_to_merge, new_merged_token, frequency_of_new_token)


        # Update the working dictionary with the new merged token
        working_dict = merge_in_working_list(working_dict, tokens_to_merge, new_merged_token)

        # Record the merging action
        merge_rules.append((tokens_to_merge, new_merged_token))

    return vocabulary, merge_rules



def main():
    if len(sys.argv) != 3:
        print("Usage: script.py <folder_path> <vocab_size>")
    #     sys.exit(1)
    #folder_path = sys.argv[1]
    #vocab_size = int(sys.argv[2])

    #folder_path = "test1/"
    #vocab_size = 1000
    folder_path = sys.argv[1]
    try:
        vocab_size = int(sys.argv[2])
    except ValueError:
        print("Please provide an integer value for vocab_size.")
        sys.exit(1)
    file_paths = list_files_in_folder(folder_path)
    token_list = []
    
    #opening each file
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            content = file.read()
            #Sending each file to removeSGML
            cleaned_content = removeSGML(content)
            # print(f"Revmoed SGL on file: {file_path}")
            #Send each cleaned file to be tokenized
            token_list.append(tokenizeText(cleaned_content))
    # print(len(token_list)) Now we have a list of list of tokens 2d list.
    
    #BPE time
    vocabulary, merge_rules = bpe(token_list, vocab_size)

    total_bpe_tokens = sum(vocabulary.values())
 # Sort tokens and merge rules by frequency
    sorted_tokens = sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)
    sorted_merge_rules = sorted(merge_rules, key=lambda rule: vocabulary.get(rule[1], 0), reverse=True)[:20]

    #calcualte sum and min tokens
    sum_tokens, min_tokens = 0, 0
    for token, freq in sorted_tokens:
        sum_tokens += freq
        min_tokens += 1
        if sum_tokens >= total_bpe_tokens * 0.25:
            break
    with open("preprocess.answers", "w") as file:
        file.write(f"Total number of BPE tokens in the Cranfield collection: {total_bpe_tokens}\n")
        file.write(f"Total number of merge rules: {len(merge_rules)}\n")
        file.write(f"The minimum number of unique BPE tokens in the Cranfield collection accounting for 25% of the total number of BPE tokens: {min_tokens}\n")

    with open("preprocess.output", "w") as file:
        # Write to the file within this block
        file.write(f"Tokens [{len(vocabulary)}]\n")
        file.write(f"Merge rules [{len(merge_rules)}]\n")

        for rule in sorted_merge_rules:
            tokens_str = ' + '.join(rule[0])  
            file.write(f"{tokens_str} -> {rule[1]}\n")

        file.write("\nTop 50 tokens\n")
        for token, freq in sorted(vocabulary.items(), key=lambda x: x[1], reverse=True)[:50]:
            file.write(f"{token}: {freq}\n")


def open_file(file_name):
    input_file = open(file_name, 'r')
    return input_file



if __name__ == "__main__":
    import sys
    main()
