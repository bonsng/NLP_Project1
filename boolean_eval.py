# Q1. Love and Breakup
# query : love & (gone | goodbye | bye | farewell | (break & (up | apart)))
from boolean_model import boolean_model
query1 = "love & (gone | goodbye | bye | farewell | (break & (up | apart)))"
query1_relevant = ['2012-Payphone-Maroon_5.txt', '2013-I_Love_It-Icona_Pop.txt', '2010-Break_Your_Heart-Taio_Cruz.txt', '2010-Alejandro-Lady_Gaga.txt', '2015-Elastic_Heart-Sia.txt', "2011-DJ_Got_Us_Fallin'_In_Love-Usher.txt", '2010-Mine-Taylor_Swift.txt', '2010-Already_Gone-Kelly_Clarkson.txt', '2013-Little_Talks-Of_Monsters_And_Men.txt', '2010-Breakeven-Script.txt', '2013-Gone,_Gone,_Gone-Phillip_Phillips.txt',
                   '2015-Thinking_Out_Loud-Ed_Sheeran.txt', '2010-There_Goes_My_Baby-Usher.txt', "2015-Like_I'm_Gonna_Lose_You-Meghan_Trainor.txt", '2010-Baby-Justin_Bieber.txt', '2013-Troublemaker-Olly_Murs.txt', '2014-Story_Of_My_Life-One_Direction.txt', '2013-Wrecking_Ball-Miley_Cyrus.txt', '2013-Mirrors-Justin_Timberlake.txt', '2012-50_Ways_To_Say_Goodbye-Train.txt', '2014-Wrecking_Ball-Miley_Cyrus.txt', '2011-Back_To_December-Taylor_Swift.txt']
queries = [query1]


def evaluate(retrieved, relevant):
    retrieved_set = set(retrieved)
    relevant_set = set(relevant)

    tp = len(retrieved_set & relevant_set)
    fp = len(retrieved_set - relevant_set)
    fn = len(relevant_set - retrieved_set)

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

    return precision, recall, f1, tp, fp, fn


if __name__ == "__main__":
    path = "./data/*"
    boolean = boolean_model(path)
    print("Song Lyrics IR (2010-2015 Billboard Top 100 Songs)")
    print("Boolean Model Evaluation")
    print("1. Love & Break Up")
    print("2. Empowerment")
    print("3. Party & Dance")
    query_num = int(input(">> "))

    print("Evaluating query:", queries[query_num-1])
    matching_docs = boolean.query(queries[query_num-1])

    # Evaluation
    precision, recall, f1, tp, fp, fn = evaluate(matching_docs, query1_relevant)

    print("Evaluation")
    print(f"TP: {tp}")
    print(f"FP: {fp}")
    print(f"FN: {fn}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F-measure: {f1:.2f}")
