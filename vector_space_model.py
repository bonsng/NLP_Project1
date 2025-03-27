import glob
import math
import re
import sys
import os
from collections import defaultdict
from functools import reduce

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


SONGS = "songs/*"


class vector_space_model(object):

    def __init__(self, path):
        self.SONGS = path
        self.STOPWORDS = set(stopwords.words("english"))
        self.songs_filename = dict()
        self.size = 0
        self.vocabulary = set()
        self.postings = defaultdict(dict)
        self.document_frequency = defaultdict(int)
        self.lengths = defaultdict(float)

        self.__preprocessing()

    def __preprocessing(self):
        """Preprocessing"""
        self.__get_songs()

        self.__initialize_postings()

        self.__initialize_frequency()

        self.__initialize_lengths()

    def __get_songs(self):
        documents = glob.glob(self.SONGS)
        self.size = len(documents)
        self.songs_filename = dict(zip(range(self.size), [os.path.basename(doc) for doc in documents]))

    def __initialize_postings(self):
        for id in self.songs_filename:
            with open("./data/"+self.songs_filename[id], "r") as f:
                document = f.read()

            document = self.remove_special_characters(document)
            document = self.remove_digits(document)

            terms = self.tokenize(document)
            unique_terms = set(terms)

            self.vocabulary = self.vocabulary.union(unique_terms)

            for term in unique_terms:
                self.postings[term][id] = terms.count(term)

    def __initialize_frequency(self):
        for term in self.vocabulary:
            self.document_frequency[term] = len(self.postings[term])

    def __initialize_lengths(self):
        for id in self.songs_filename:
            l = 0
            for term in self.vocabulary:
                if id in self.postings[term]:
                    l += self.postings[term][id] ** 2

            self.lengths[id] = math.sqrt(l)

    def do_search(self, query):
        query = self.tokenize(query)

        if query == []:
            sys.exit()

        scores = sorted(
            [(id, self.cosine_similarity(query, id)) for id in range(self.size)],
            key=lambda x: x[1],
            reverse=True,
        )

        self.print_scores(scores)

    def tf(self, term, id):
        if id in self.postings[term]:
            return self.postings[term][id]
        else:
            return 0.0

    def idf(self, term):
        if term in self.vocabulary:
            return math.log(self.size / self.document_frequency[term], 2)
        else:
            return 0.0

    def cosine_similarity(self, query, id):
        similarity = 0.0

        for term in query:
            if term in self.vocabulary:
                similarity += self.tf(term, id) * self.idf(term)

        similarity = similarity / self.lengths[id]

        return similarity

    def print_scores(self, scores):
        print("%s | %-40s" % ("Score", "Song"))
        print("-" * 52)
        print(f"{'Score':<8}{'Title':<30}{'Artist':<25}{'Year'}")
        print("-" * 60)

        for (id, score) in scores:
            if score != 0.0:
                year, title, artist = self.songs_filename[id].split("-", 2)
                artist = artist.replace(".txt", "")
                artist = artist.replace("_", " ")
                title = title.replace("_", " ")
                print(f"{str(score)[:5]:<8}{title:<30}{artist:<25}{year}")
        print(end="\n")

    def remove_special_characters(self, text):
        """Removes special characters from text"""
        regex = re.compile(r"[^a-zA-Z0-9\s]")
        return re.sub(regex, "", text)

    def remove_digits(self, text):
        """Removes digits from text"""
        regex = re.compile(r"\d")
        return re.sub(regex, "", text)

    def tokenize(self, document):
        terms = word_tokenize(document)
        terms = [term.lower() for term in terms if term not in self.STOPWORDS]
        return terms
