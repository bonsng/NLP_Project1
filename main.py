from boolean_model import boolean_model
from vector_space_model import vector_space_model
from latent_semantic_indexing import latent_semantic_indexing

if __name__ == "__main__":
    path = "./data/*"
    print("Song Lyrics IR (2010-2015 Billboard Top 100 Songs)")
    print("1. Boolean Model\n2. Vector Space Model\n3. LSI")
    n = input("(1/2/3)>> ")

    if n == "1":
        boolean = boolean_model(path)
        while True:
            query = input("Type Query for search (AND: & / OR: | / NOT: ~)\n>>> ")
            matching_docs = boolean.query(query)
    elif n == "2":
        vector_model = vector_space_model(path)
        while True:
            query = input("Enter Query\n>> ")
            vector_model.do_search(query)
    elif n == "3":
        while True:
            query = input("Enter Query\n>> ")
            lsi_50 = latent_semantic_indexing(path, 50)
            lsi_50.do_search(query)
    else:
        print("Invalid Input")
