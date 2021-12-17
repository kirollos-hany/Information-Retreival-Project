from PostingEntry import PostingEntry


class IndexKey:
    def __init__(self, term, document_frequency):
        self.term = term
        self.df = document_frequency

    def __hash__(self):
        return hash(self.term)

    def __eq__(self, other):
        return self.term == other.term
