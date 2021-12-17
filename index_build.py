import sys
sys.path.append('./classes/')
from IndexKey import IndexKey
from PostingEntry import PostingEntry
from utils import read_doc, get_docs_count, posting_entry_sort_key, write_pos_index_todisk
from preprocessing import preprocess
import pandas as pd



docs_count = get_docs_count()
docs = []
for i in range(1, docs_count + 1):
    preprocessed_doc = ' '.join(preprocess(read_doc(i)))
    docs.append(preprocessed_doc)


def get_docs_terms(docs):
    terms = []
    for doc_content in docs:
        doc_tokens_series = pd.Series(doc_content.split())
        doc_tokens_series.drop_duplicates(keep='first', inplace=True)
        for token in doc_tokens_series:
            terms.append(token)
    terms_series = pd.Series(terms)
    terms_series = terms_series.drop_duplicates(keep='first', inplace=False).dropna()
    return terms_series


def get_term_df(term, docs):
    df = 0
    for doc_content in docs:
        if term in doc_content.split():
            df += 1
    return df


def get_term_postings(term, docs):
    postings = []
    pos = 0
    doc_id = 0
    for doc_content in docs:
        doc_id += 1
        posting_entry = PostingEntry(0, [])
        tokens = doc_content.split()
        pos = 0
        for token in tokens:
            pos += 1
            if term == token:
                posting_entry.doc_id = doc_id
                posting_entry.term_positions.append(pos)
        if(posting_entry.doc_id != 0):
            posting_entry.term_positions.sort()
            postings.append(posting_entry)
            postings.sort(key=posting_entry_sort_key)
    return postings


def build_pos_index(terms_series, docs):
    index = {}
    for term in terms_series:
        term_df = get_term_df(term, docs)
        term_postings = get_term_postings(term, docs)
        index_key = IndexKey(term, term_df)
        index[index_key] = term_postings
    return index


index = build_pos_index(get_docs_terms(docs), docs)

write_pos_index_todisk(index)


