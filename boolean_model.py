import glob
import os
import re
import sys

from collections import defaultdict
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from query import infix_to_postfix
from stack import Stack


class boolean_model(object):

    def __init__(self, path):
        self.SONGS = path
        self.STOPWORDS = set(stopwords.words("english"))
        self.word_dict = defaultdict(list)
        self.songs = dict()
        self.vocabulary = set()

        self.__preprocessing()

    def __preprocessing(self):
        """Preprocessing: remove characters/digits and tokenize words"""

        idx = 1
        for filename in glob.glob(self.SONGS):

            with open(filename, "r") as f:
                text = f.read()

            text = self.remove_special_characters(text)
            text = self.remove_digits(text)
            words = word_tokenize(text)
            words = [word.lower() for word in words if word not in self.STOPWORDS]
            unique_words = list(set(words))

            for unique_word in unique_words:
                self.word_dict[unique_word].append(idx)

            self.songs[idx] = os.path.basename(filename)

            idx += 1

        self.vocabulary = self.word_dict.keys()
        return

    def query(self, query):
        query_tokens = word_tokenize(query)

        if query_tokens == []:
            sys.exit()

        query_tokens = infix_to_postfix(query_tokens)

        matching_docs = self.__query_process(query_tokens)

        print(f"{'No.':<6}{'Year':<8}{'Artist':<20}{'Title'}")
        print("-" * 60)
        for idx, song_file in enumerate(matching_docs, 1):
            try:
                year, title, artist = song_file.split("-", 2)
                artist = artist.replace(".txt", "")
                artist = artist.replace("_", " ")
                title = title.replace("_", " ")
                print(f"{idx:<6}{year:<8}{artist:<20}{title}")
            except ValueError:
                print(f"{idx:<6}{'Unknown':<8}{'Unknown':<20}{song_file}")

        print(end="\n")

    def __query_process(self, query_tokens):
        operands = Stack()

        for token in query_tokens:
            if token == "&":
                right = operands.pop()
                left = operands.pop()
                operands.push(self.__and_merge(left, right))
            elif token == "|":
                right = operands.pop()
                left = operands.pop()
                operands.push(self.__or_merge(left, right))
            else:
                token = token.lower()
                operands.push(self.__get_posting(token))

        if len(operands) != 1:
            print("Error: Wrong Query")
            return list()

        matching_docs = operands.pop()
        return [self.songs[doc_id] for doc_id in matching_docs]

    def __and_merge(self, left, right):
        """AND operation"""
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] == right[j]:
                result.append(left[i])
                i += 1
                j += 1
            elif left[i] < right[j]:
                i += 1
            else:
                j += 1
        return result

    def __or_merge(self, left, right):
        """OR operation"""
        result = []
        i, j = 0, 0
        while i < len(left) and j < len(right):
            if left[i] == right[j]:
                result.append(left[i])
                i += 1
                j += 1
            elif left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def __not_merge(self, posting, all_docs):
        """NOT operation"""
        result = []
        i, j = 0, 0
        while i < len(all_docs) and j < len(posting):
            if all_docs[i] == posting[j]:
                i += 1
                j += 1
            elif all_docs[i] < posting[j]:
                result.append(all_docs[i])
                i += 1
            else:
                j += 1
        result.extend(all_docs[i:])
        return result

    def __get_posting(self, token):
        negate = False

        if token[0] == "~":
            negate = True
            token = token[1:]

        postings = sorted(self.word_dict.get(token, []))

        if negate:
            all_docs = sorted(self.songs.keys())
            return self.__not_merge(postings, all_docs)

        return postings

    def remove_special_characters(self, text):
        """Removes special characters from text"""
        regex = re.compile(r"[^a-zA-Z0-9\s]")
        return re.sub(regex, "", text)

    def remove_digits(self, text):
        """Removes digits from text"""
        regex = re.compile(r"\d")
        return re.sub(regex, "", text)
