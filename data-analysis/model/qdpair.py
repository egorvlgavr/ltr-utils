class QueryDocumentPair:
    def __init__(self, query, document):
        self.query = query
        self.doc_id = document

    def __eq__(self, o) -> bool:
        return (self.__class__ == o.__class__
                and self.query == o.query
                and self.doc_id == o.doc_id)

    def __hash__(self) -> int:
        return hash((self.query, self.doc_id))

    def __str__(self) -> str:
        return str((self.query, self.doc_id))
