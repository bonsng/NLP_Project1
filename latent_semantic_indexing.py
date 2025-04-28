import glob
import re
import sys
import os
import numpy as np
from nltk.tokenize import word_tokenize
from scipy.linalg import svd


class latent_semantic_indexing(object):
    def __init__(self, path, rank=100):
        self.SONGS = path
        self.songs_filename = dict()
        self.size = 0
        self.vocabulary = []
        self.term_to_index = dict()
        self.index_to_term = dict()
        self.rank = rank

        self.A = None
        self.U = None
        self.S = None
        self.Vt = None

        self.__preprocessing()

    def __preprocessing(self):
        """Preprocessing"""
        self.__get_songs()
        self.__build_term_document_matrix()
        self.__apply_svd()

    def __get_songs(self):
        documents = glob.glob(self.SONGS)
        self.size = len(documents)
        self.songs_filename = dict(zip(range(self.size), [os.path.basename(doc) for doc in documents]))

    def __build_term_document_matrix(self):
        documents = []
        vocab_set = set()

        for id in range(self.size):
            with open("./data/" + self.songs_filename[id], "r") as f:
                document = f.read()

            document = self.remove_special_characters(document)
            document = self.remove_digits(document)

            terms = self.tokenize(document)
            documents.append(terms)
            vocab_set.update(terms)

        self.vocabulary = sorted(list(vocab_set))
        self.term_to_index = {term: idx for idx, term in enumerate(self.vocabulary)}
        self.index_to_term = {idx: term for idx, term in enumerate(self.vocabulary)}

        A = np.zeros((len(self.vocabulary), self.size))

        for doc_id, terms in enumerate(documents):
            for term in terms:
                term_idx = self.term_to_index[term]
                A[term_idx][doc_id] += 1

        self.A = A

    def __apply_svd(self):
        """Decompose matrix A and truncate to rank k"""
        U, S, Vt = svd(self.A, full_matrices=False)

        # Truncate to rank-k
        k = min(self.rank, len(S))
        self.U = U[:, :k]
        self.S = np.diag(S[:k])
        self.Vt = Vt[:k, :]

    def do_search(self, query):
        query_vector = self.__transform_query(query)

        if query_vector is None:
            print("Query is empty after preprocessing.")
            sys.exit()

        # Step 5: Find the new query vector coordinates in the reduced 2-dimensional space.
        query_lsi = query_vector @ self.U @ np.linalg.inv(self.S)

        scores = []
        for doc_id in range(self.size):
            doc_vector = self.Vt[:, doc_id]
            score = self.__cosine_similarity(query_lsi, doc_vector)
            scores.append((doc_id, score))

        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        self.print_scores(scores[:10])

    def __transform_query(self, query):
        """Transform a query into a TF vector"""
        query = self.tokenize(query)

        if len(query) == 0:
            return None

        q_vec = np.zeros(len(self.vocabulary))
        for term in query:
            if term in self.term_to_index:
                idx = self.term_to_index[term]
                q_vec[idx] += 1

        return q_vec

    def __cosine_similarity(self, vec1, vec2):
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0.0
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def print_scores(self, scores):
        print(f"LSI retrieval : Rank-{self.rank}")
        print("-" * 70)
        print(f"{'Score':<8}{'Title':<30}{'Artist':<25}{'Year'}")
        print("-" * 70)

        for (id, score) in scores:
            if score != 0.0:
                year, title, artist = self.songs_filename[id].split("-", 2)
                artist = artist.replace(".txt", "")
                artist = artist.replace("_", " ")
                title = title.replace("_", " ")
                print(f"{str(score)[:5]:<8}{title:<30}{artist:<25}{year}")
        print(end="\n")

    def remove_special_characters(self, text):
        regex = re.compile(r"[^a-zA-Z0-9\s]")
        return re.sub(regex, "", text)

    def remove_digits(self, text):
        regex = re.compile(r"\d")
        return re.sub(regex, "", text)

    def tokenize(self, document):
        terms = word_tokenize(document)
        terms = [term.lower() for term in terms]
        return terms

    def print_document_coordinates(self):
        print("Document Coordinates in Latent Semantic Space:")
        for doc_id in range(self.size):
            coord = self.Vt[:, doc_id]
            print(f"{self.songs_filename[doc_id]} -> ({coord[0]:.4f}, {coord[1]:.4f})")
