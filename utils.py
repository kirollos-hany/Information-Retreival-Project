import os
import sys
sys.path.append('./classes/')
import math
from IndexKey import IndexKey
from PostingEntry import PostingEntry

def read_doc(doc_id):
    with open(f'./docs/{doc_id}.txt', 'r') as doc:
        return doc.read()

def get_docs_count():
    doc_count = 0
    for base, dirs, files in os.walk('./docs/'):
        for Files in files:
            doc_count += 1
    return doc_count

def posting_entry_sort_key(posting_entry):
    return posting_entry.doc_id


def write_pos_index_todisk(index):
    result = []
    for index_key in index:
        index_record_str = f'{index_key.term}-{index_key.df}:'
        for posting in index[index_key]:
            index_record_str += f'({posting.doc_id}-'
            for pos in posting.term_positions:
                index_record_str += f'{pos},'
            index_record_str += f')'
        index_record_str += '\n'
        result.append(index_record_str)
    with open('./output/pos_index.txt', 'w') as index_file:
        for index in result:
            index_file.write(index)

def write_vector_model_todisk(vector_model):
    result = []
    for term in vector_model:
        record_str = f'{term}: '
        for tfidf in vector_model[term]:
            record_str += f'{tfidf} '
        record_str += '\n'
        result.append(record_str)
    with open('./output/vector_model.txt', 'w') as file:
        for record in result:
            file.write(record)

def read_vector_model_fromdisk():
    vector_model = {}
    with open('./output/vector_model.txt', 'r') as file:
        for record in file:
            term_tfidfs_split = record.split(':')
            term = term_tfidfs_split[0]
            tfidfs = [float(tfidf) for tfidf in term_tfidfs_split[1].split()]
            vector_model[term] = tfidfs
    return vector_model
            
def read_pos_index_fromdisk():
    index = {}
    with open('./output/pos_index.txt', 'r') as index_file:
        for record in index_file:
            term_df_postings_split = record.split(':')
            term_df = term_df_postings_split[0]
            term_df_split = term_df.split('-')
            index_key = IndexKey(term_df_split[0], int(term_df_split[1]))
            postings = []
            postings_str = term_df_postings_split[1]
            posting_entry = PostingEntry(0, [])
            for char_indx in range(len(postings_str)):
                char = postings_str[char_indx]
                if char == '-':
                    posting_entry.doc_id = int(postings_str[char_indx - 1])
                elif char == ',':
                    posting_entry.term_positions.append(int(postings_str[char_indx - 1]))
                elif char == ')':
                    postings.append(posting_entry)
                    posting_entry = PostingEntry(0, [])
            index[index_key] = postings
    return index

def read_term_postings_fromdisk(term):
    postings = []
    with open('./output/pos_index.txt', 'r') as file:
        for line in file:
            term_df_postings_split = line.split(':')
            term_df_split = term_df_postings_split[0].split()
            read_term = term_df_split[0].split('-')[0]
            if read_term == term:
                postings_str = term_df_postings_split[1]
                posting_entry = PostingEntry(0, [])
                for indx in range(len(postings_str)):
                    char = postings_str[indx]
                    if char == '-':
                        posting_entry.doc_id = int(postings_str[indx - 1])
                    elif char == ',':
                        posting_entry.term_positions.append(int(postings_str[indx - 1]))
                    elif char == ')':
                        postings.append(posting_entry)
                        posting_entry = PostingEntry(0, [])
    return postings


def read_terms_fromdisk():
    terms = []
    with open('./output/pos_index.txt', 'r') as file:
        for line in file:
            term_df_postings_split = line.split(':')
            term_df = term_df_postings_split[0]
            term = term_df.split('-')[0]
            terms.append(term)
    return terms

def compute_tfidf(df, tf, docs_count):
    idf = math.log(docs_count / df, 10)
    log_tf = math.log(1 + tf, 10)
    return log_tf * idf


    
    


            


             
                    
                    
                
                    
                
            

        
    
    

        
    
    


        