from utils import read_pos_index_fromdisk, read_vector_model_fromdisk, get_docs_count, compute_tfidf
from preprocessing import preprocess
from phrase_search import phrase_query_search
from numpy import dot
from numpy.linalg import norm

pos_index = read_pos_index_fromdisk()
vector_model = read_vector_model_fromdisk()
docs_count = get_docs_count()

def display_pos_index(index):
    i = 0
    for key in index:
        print(f'term{i + 1}: {key.term} df: {key.df} postings:', end = ' ')
        for posting in index[key]:
            print(f'doc-id: {posting.doc_id} positions: {posting.term_positions}')
        print()
        i += 1

def display_search_result(result):
    print('Matching documents:', end=" ")
    for res in result:
        print(f'{res[0]},', end = " ")
    print()

def display_tfidf_matrix(vector_model, docs_count):
    print('\t', end="")
    for i in range(1, docs_count + 1):
        print(f'doc{i}', end='\t')
    print()
    for term in vector_model:
        print(f'{term}:', end = " ")
        for tfidf in vector_model[term]:
            formatted_tfidf = "{:10.4f}".format(tfidf)
            print(f'{formatted_tfidf}', end="\t")
        print()
        
def construct_query_vector(processed_query, pos_indx, docs_count):
    query_vector = []
    keys = pos_indx.keys()
    for key in keys:
        term_frequency = 0
        for word in processed_query:
            if word == key.term:
                term_frequency += 1
        query_vector.append(compute_tfidf(key.df, term_frequency, docs_count))
    return query_vector

def get_doc_vector(doc_id, vector_model):
    doc_vector = []
    for term in vector_model:
        doc_vector.append(vector_model[term][doc_id - 1])
    return doc_vector

def compute_cos_sim(v1, v2):
    return dot(v1, v2) / norm(v1) * norm(v2)

def sort_result_by_rank(search_result, query_vector, vector_model):
    ranked_docs = {}
    for result in search_result:
        doc_vector = get_doc_vector(result[0], vector_model)
        score = compute_cos_sim(query_vector, doc_vector)
        ranked_docs[result[0]] = score
    ranked_docs = {k :v for k, v in sorted(ranked_docs.items(), key= lambda item: item[1], reverse=True)}
    return ranked_docs

if __name__ == '__main__':
    choices = ['--IR Menu--','1-Display positional index','2-Display TF-IDF matrix', '3-Perform phrase search', '4-Exit']
    cont_flag = True
    while cont_flag:
        for choice in choices:
            print(choice)
        try:
            user_choice = int(input("Please enter your choice:\n"))
            if user_choice == 1:
                display_pos_index(pos_index)
            elif user_choice == 2:
                display_tfidf_matrix(vector_model, docs_count)
            elif user_choice == 3:
                phrase = input("Enter phrase:\n")
                processed_phrase = preprocess(phrase)
                search_result = phrase_query_search(processed_phrase)
                if(len(search_result) == 0):
                    print(f'Sorry, no matches found')
                else:
                    query_vector = construct_query_vector(processed_phrase, pos_index, docs_count)
                    ranked_docs = sort_result_by_rank(search_result, query_vector, vector_model)
                    print('Matched documents:')
                    for doc_id in ranked_docs:
                        formatted_score = "{:10.4f}".format(ranked_docs[doc_id])
                        print(f'doc{doc_id} score:{formatted_score}')
            elif user_choice == 4:
                cont_flag = False
        except ValueError:
            print('Invalid choice, please try again')
            continue