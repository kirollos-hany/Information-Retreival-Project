from utils import get_docs_count, read_pos_index_fromdisk, write_vector_model_todisk, compute_tfidf

pos_indx = read_pos_index_fromdisk()

docs_count = get_docs_count()

def build_vector_model(pos_indx, docs_count):
    term_doc_tfidf_dict = {}
    docs_range = range(1, docs_count + 1)
    for key in pos_indx:
        term = key.term
        term_df = key.df
        term_postings = pos_indx[key]
        term_doc_tfidf_dict[term] = []
        for doc_id in docs_range:
            term_freq = 0
            for posting in term_postings:
                if posting.doc_id == doc_id:
                    term_freq = len(posting.term_positions)
                    break
            tfidf = compute_tfidf(term_df, term_freq, docs_count)
            term_doc_tfidf_dict[term].append(tfidf)
    return term_doc_tfidf_dict

vector_model = build_vector_model(pos_indx, docs_count)

write_vector_model_todisk(vector_model)

            
        
    
    

