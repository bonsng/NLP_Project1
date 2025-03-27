from boolean_model import boolean_model
from vector_space_model import vector_space_model

if __name__ == "__main__":
    path = "./data/*"
    boolean = boolean_model(path)
    vector_model = vector_space_model(path)
    print("Song Lyrics IR (2010-2015 Billboard Top 100 Songs)")
    print("1. Boolean Model\n2. Vector Space Model")
    n = input("(1/2)>> ")

    if n == "1":
        while True:
            query = input("Type Query for search (AND: & / OR: | / NOT: ~)\n>>> ")
            boolean.query(query)
    elif n == "2":
        while True:
            query = input("Enter Query\n>> ")
            vector_model.do_search(query)
    else:
        print("Invalid Input")
