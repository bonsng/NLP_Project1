# NLP Project 1

- [Introduction](#introduction)
- [Data](#data--2010-2015-billboard-top-100-songs-txt)
- [Getting Started](#getting-started)
- [Evaluation](#evaluation)
- [LSI](#lsi)
- [Reference](#reference)


---
## Introduction
### Song Lyrics IR System (Boolean & Vector Space Model)

`boolean_model.py` : boolean model

`vector_space_model.py` : vector space model

`boolean_eval.py` : boolean model evaluation

`latent_semantic_indexing.py` : LSI model

---

### Data : 2010-2015 Billboard Top 100 Songs (.txt)

- Actual Data: in the _/data_ folder
- Data source: Top 100 Songs & Lyrics By Year (https://www.kaggle.com/datasets/brianblakely/top-100-songs-and-lyrics-from-1959-to-2019)

---

### Getting Started

- Install Python 3.6+
- Install pip requirements(nltk):

```bash
$ python -m pip install -r requirements.txt
$ pip install nltk
```

- To download stopwords used for the model, open your terminal or command prompt and enter following commands:

```bash
$ python
>>> import nltk
>>> nltk.download('stopwords')
```

- Run main.py

```bash
$ python main.py
```

- Choose model to use

```bash
Song Lyrics IR (2010-2015 Billboard Top 100 Songs)
1. Boolean Model
2. Vector Space Model
3. LSI
>>
```

---
### Evaluation

- Run boolean_eval.py

```bash
$ python boolean_eval.py
```

- Choose query to evaluate

```bash
Boolean Model Evaluation
1. Love & Break Up
2. Empowerment
3. Party & Dance
>>
```

---
### LSI

- Run main.py and choose LSI(#3)
- Enter query to search
```bash
$ python main.py
Song Lyrics IR (2010-2015 Billboard Top 100 Songs)
1. Boolean Model
2. Vector Space Model
3. LSI
(1/2/3)>> 3
Enter Query
>>
```

---

### Reference

- [Github(boolean-retrieval-model)](https://github.com/mayank-02/boolean-retrieval-model/tree/main)
- [Github(vector-space-model)](https://github.com/mayank-02/boolean-retrieval-model/tree/main)
- [WikiDocs(LSA)](https://wikidocs.net/24949)
- [Datacamp(Python LSO/LSA)](https://www.datacamp.com/tutorial/discovering-hidden-topics-python)
- OpenAI. (2025). ChatGPT (4o version) [Large language model].
