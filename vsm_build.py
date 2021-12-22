from utils import get_docs_count, read_pos_index_fromdisk, compute_idf
import math
from numpy import dot

pos_indx = read_pos_index_fromdisk()

docs_count = get_docs_count()

def build_tf_matrix(pos_index, docs_count):
    tf_matrix = []
    tf_dict = {}
    for i in range(1, docs_count + 1):
            tf_dict[i] = 0
    for key in pos_index:
        line = f"{key.term} "
        for posting in pos_index[key]:
            tf = len(posting.term_positions)
            doc_id = posting.doc_id
            tf_dict[doc_id] = tf
        for key in tf_dict:
            line += f"{tf_dict[key]} "
        line += "\n"
        tf_matrix.append(line)
        for i in range(1, docs_count + 1):
            tf_dict[i] = 0
    return tf_matrix

def build_wtf_matrix(pos_index, docs_count):
    tf_matrix = []
    tf_dict = {}
    for i in range(1, docs_count + 1):
            tf_dict[i] = 0
    for key in pos_index:
        line = f"{key.term} "
        for posting in pos_index[key]:
            tf = 1 + math.log(len(posting.term_positions), 10)
            doc_id = posting.doc_id
            tf_dict[doc_id] = tf
        for key in tf_dict:
            line += f"{tf_dict[key]} "
        line += "\n"
        tf_matrix.append(line)
        for i in range(1, docs_count + 1):
            tf_dict[i] = 0
    return tf_matrix
        
def build_df_idf(pos_index, docs_count):
    df_idf = []
    for key in pos_index:
        term = key.term
        df = key.df
        idf = compute_idf(df, docs_count)
        df_idf.append(f"{term} df:{df} idf:{idf}\n")
    return df_idf

def build_tf_idf(pos_index, docs_count):
    tf_idf = []
    tf_idf_dict = {}
    for i in range(1, docs_count + 1):
        tf_idf_dict[i] = 0
    for key in pos_index:
        line = f"{key.term} "
        for posting in pos_index[key]:
            tf = 1 + math.log(len(posting.term_positions), 10)
            idf = compute_idf(key.df, docs_count)
            tf_idf_dict[posting.doc_id] = tf * idf
        for _key in tf_idf_dict:
            line += f"{tf_idf_dict[_key]} "
        line += "\n"
        tf_idf.append(line)
        for i in range(1, docs_count + 1):
            tf_idf_dict[i] = 0
    return tf_idf

def build_doc_length(pos_index, docs_count):
    doc_lengths = []
    tf_idf_matrix = build_tf_idf(pos_index, docs_count)
    for i in range(1, docs_count + 1):
        tf_idf_sum = 0
        for tf_idf in tf_idf_matrix:
            tokens = tf_idf.split(' ')
            tf_idf_sum += float(tokens[i]) ** 2
        doc_lengths.append(math.sqrt(tf_idf_sum))
    return doc_lengths

def write_doc_length(doc_lengths):
    with open('./output/doc_lengths.txt', 'w') as file:
        doc_id = 1
        for line in doc_lengths:
            full_line = f"doc{doc_id} {line}\n"
            file.write(full_line)
            doc_id += 1

def build_normalized_tfidf(pos_index, docs_lengths, docs_count, tfidf_matrix):
    normalized_tfidfs = []
    index_keys = list(pos_index.keys())
    term_ptr = 0
    for tfidf_line in tfidf_matrix:
        doc_ptr = 1
        line = f"{index_keys[term_ptr].term} "
        while doc_ptr <= docs_count:
            tfidf_split = tfidf_line.split(' ')
            tfidf = float(tfidf_split[doc_ptr])
            normalized_tfidf = tfidf / docs_lengths[doc_ptr - 1]
            line += f"{normalized_tfidf} "
            doc_ptr += 1
        line += "\n"
        normalized_tfidfs.append(line)
        term_ptr += 1
    return normalized_tfidfs

def write_output_file(file_name, lines):
    with open(f'./output/{file_name}.txt', 'w') as file:
        for line in lines:
            file.write(line)

def construct_query_vector(processed_query, df_idf_matrix):
    term_tf_dict = {}
    query_vector = []
    print("Constructing query vector:")
    for term in processed_query:
        term_tf_dict[term] = 0
    for term in processed_query:
        term_tf_dict[term] += 1
    for key in term_tf_dict:
        print(f"term:{key} tf:{term_tf_dict[term]}")
        term_tf_dict[key] = 1 + math.log(term_tf_dict[key], 10)
        print(f"term:{key} wtf:{term_tf_dict[key]}")
    print("Query tf-idf vector:")
    ctr = 0
    for line in df_idf_matrix:
        line_split = line.split(' ')
        term = line_split[0]
        if term in processed_query:
            wtf = term_tf_dict[term]
            idf = line_split[2].split(':')[1]
            query_vector.append(wtf * float(idf))
        else:
            query_vector.append(0)
        print(f"{term} {query_vector[ctr]}")
        ctr += 1
    query_sq_sum = 0
    for wtf_idf in query_vector:
        query_sq_sum += wtf_idf ** 2
    query_vect_length = math.sqrt(query_sq_sum)
    print(f"Query vector length:{query_vect_length}")
    print("Normalized query vector:")
    query_vect_ptr = 0
    for wtf_idf in query_vector:
        query_vector[query_vect_ptr] = wtf_idf / query_vect_length
        print(query_vector[query_vect_ptr])
        query_vect_ptr += 1
    return query_vector

def rank_result_docs(query_vector, result_docs, normalized_tfidf):
    result_docs_scores = []
    for result in result_docs:
        doc_id = result[0]
        norm_doc_vector = []
        for line in normalized_tfidf:
            line_split = line.split(' ')
            norm_doc_vector.append(line_split[doc_id])
        for i in range(len(norm_doc_vector)):
            norm_doc_vector[i] = float(norm_doc_vector[i])
        score = dot(query_vector, norm_doc_vector)
        doc_score_tuple = (doc_id, score)
        result_docs_scores.append(doc_score_tuple)
        result_docs_scores.sort(key = lambda x : x[1], reverse=True)
    return result_docs_scores

df_idf = build_df_idf(pos_indx, docs_count)
write_output_file('df_idf',df_idf)

tf_matrix = build_tf_matrix(pos_indx, docs_count)
write_output_file('tf_matrix',tf_matrix)

wtf_matrix = build_wtf_matrix(pos_indx, docs_count)
write_output_file('wtf_matrix',wtf_matrix)

tf_idf_matrix = build_tf_idf(pos_indx, docs_count)
write_output_file('tf_idf',tf_idf_matrix)

doc_lengths = build_doc_length(pos_indx, docs_count)
write_doc_length(doc_lengths)

normalized_tfidfs = build_normalized_tfidf(pos_indx, doc_lengths, docs_count, tf_idf_matrix)
write_output_file('normalized_tfidf',normalized_tfidfs)

            
        
    
    

