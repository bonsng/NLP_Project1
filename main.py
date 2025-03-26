from boolean_model import boolean_model
from vector_space_model import vector_space_model

if __name__ == "__main__":
    boolean = boolean_model("./songs/*")
    vector_model = vector_space_model("./songs/*")
    print("Song Lyrics IR")
    print("1. Boolean Model\n2. Vector Space Model")
    n = input("(1/2)>> ")

    if n == "1":
        result = boolean.query(input("Type Query for search (AND: & / OR: | / NOT: ~)\n>>> "))
        print(f"Result: {len(result)} songs")
        for idx, doc in enumerate(result, 1):
            print(f"{idx}. {doc}")
    elif n == "2":
        while True:
            query = input("Enter Query\n>> ")
            vector_model.do_search(query)
    else:
        print("Invalid Input")
