from utils import read_pos_index_fromdisk, get_docs_count, read_output_file
from preprocessing import preprocess
from phrase_search import phrase_query_search
from vsm_build import construct_query_vector, rank_result_docs


pos_index = read_pos_index_fromdisk()
docs_count = get_docs_count()
tf_matrix = read_output_file('tf_matrix')
wtf_matrix = read_output_file('wtf_matrix')
df_idf_matrix = read_output_file('df_idf')
docs_lengths = read_output_file('doc_lengths')
normalized_tfidf = read_output_file('normalized_tfidf')

def display_pos_index(index):
    i = 0
    for key in index:
        print(f'term{i + 1}: {key.term} df: {key.df} postings:', end = ' ')
        for posting in index[key]:
            print(f'doc-id: {posting.doc_id} positions: {posting.term_positions}')
        print()
        i += 1

def display_tf_matrix(docs_count, tf_matrix):
    print("TF MATRIX")
    print("\t", end=" ")
    for i in range(1, docs_count + 1):
        print(f"doc{i}", end=" ")
    print()
    for line in tf_matrix:
        print(line)

def display_wtf_matrix(docs_count, wtf_matrix):
    print("W TF MATRIX")
    print("\t", end=" ")
    for i in range(1, docs_count + 1):
        print(f"doc{i}", end=" ")
    print()
    for line in wtf_matrix:
        print(line)

def display_df_idf_matrix(docs_count, df_idf_matrix):
    print("DF IDF MATRIX")
    print("\t", end=" ")
    for i in range(1, docs_count + 1):
        print(f"doc{i}", end=" ")
    print()
    for line in df_idf_matrix:
        print(line)

def display_doc_lengths(docs_lengths):
    print("DOCS LENGTHS")
    for line in docs_lengths:
        print(line)

def display_normalized_tfidf(normalized_tfidf):
    print("NORMALIZED TF IDF MATRIX")
    for line in normalized_tfidf:
        print(line)

def display_result_docs(result_docs_scores):
    print("Resulting documents and their cosine similarity score:")
    for result in result_docs_scores:
        print(f"Doc{result[0]} Score:{result[1]}")
        
if __name__ == '__main__':
    choices = ['1-display positional index', '2-display tf matrix'
               , '3-display wtf matrix', '4-display df idf matrix',
               '5-display doc lengths', '6-display normalized tfidf',
               '7-perform phrase search', '8-exit']
    cont_flag = True
    while cont_flag:
         try:
            for choice in choices:
                print(choice)
            user_choice = int(input("Enter your choice:\n"))
            if user_choice == 1:
                display_pos_index(pos_index)
            elif user_choice == 2:
                display_tf_matrix(docs_count)
            elif user_choice == 3:
                display_wtf_matrix(docs_count)
            elif user_choice == 4:
                display_df_idf_matrix(docs_count)
            elif user_choice == 5:
                display_doc_lengths()
            elif user_choice == 6:
                display_normalized_tfidf()
            elif user_choice == 7:
                query = input("Enter phrase to search:\n")
                processed_query = preprocess(query)
                result_docs = phrase_query_search(processed_query)
                if len(result_docs) == 0:
                    print("Sorry, no matching documents found.")
                else:
                    query_vector = construct_query_vector(processed_query, df_idf_matrix)
                    ranked_docs = rank_result_docs(query_vector, result_docs, normalized_tfidf)
                    display_result_docs(ranked_docs)
            elif user_choice == 8:
                cont_flag = False
         except ValueError:
             print("Invalid choice, please choose a number from the menu")
             continue
