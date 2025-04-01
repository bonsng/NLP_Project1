# Q1. Love and Breakup
# query : love & (gone | goodbye | bye | farewell | (break & (up | apart)))
from boolean_model import boolean_model
query1 = "love & (gone | goodbye | bye | farewell | (break & (up | apart)))"
query1_relevant = ['2012-Payphone-Maroon_5.txt', '2013-I_Love_It-Icona_Pop.txt', '2010-Break_Your_Heart-Taio_Cruz.txt', '2010-Alejandro-Lady_Gaga.txt', '2015-Elastic_Heart-Sia.txt', "2011-DJ_Got_Us_Fallin'_In_Love-Usher.txt", '2010-Mine-Taylor_Swift.txt', '2010-Already_Gone-Kelly_Clarkson.txt', '2013-Little_Talks-Of_Monsters_And_Men.txt', '2010-Breakeven-Script.txt', '2013-Gone,_Gone,_Gone-Phillip_Phillips.txt',
                   '2015-Thinking_Out_Loud-Ed_Sheeran.txt', '2010-There_Goes_My_Baby-Usher.txt', "2015-Like_I'm_Gonna_Lose_You-Meghan_Trainor.txt", '2010-Baby-Justin_Bieber.txt', '2013-Troublemaker-Olly_Murs.txt', '2014-Story_Of_My_Life-One_Direction.txt', '2013-Wrecking_Ball-Miley_Cyrus.txt', '2013-Mirrors-Justin_Timberlake.txt', '2012-50_Ways_To_Say_Goodbye-Train.txt', '2014-Wrecking_Ball-Miley_Cyrus.txt', '2011-Back_To_December-Taylor_Swift.txt']

query2 = "( strong | power ) & ( win | undefeated ) | ( rise | believe | stand )"
query2_relevant = ['2010-Not_Afraid-Eminem.txt', '2011-The_Show_Goes_On-Lupe_Fiasco.txt', '2012-Stronger-Kelly_Clarkson.txt', '2013-Roar-Katy_Perry.txt',
                   '2014-The_Man-Aloe_Blacc.txt', '2015-Fight_Song-Rachel_Platten.txt', '2015-Elastic_Heart-Sia.txt', '2015-Here-Alessia_Cara.txt', '2011-Born_This_Way-Lady_Gaga.txt', '2013-Same_Love-Macklemore.txt', '2010-I_Made_It-Kevin_Rudolf.txt']

query3 = "( party | club | tonight | weekend | celebrate ) & ( dance | dancing | move | shake | groove | dj ) & ~slow"
query3_relevant = ['2010-OMG-Usher.txt', '2010-Telephone-Lady_Gaga.txt', '2010-TiK_ToK-Ke$ha.txt', '2014-Wiggle-Jason_Derulo.txt', '2011-On_The_Floor-Jennifer_Lopez.txt', '2011-Tonight-Enrique_Iglesias.txt', '2013-Body_Party-Ciara.txt', '2011-Hey_Baby-Pitbull.txt', '2011-Blow-Ke$ha.txt', '2010-I_Gotta_Feeling-Black_Eyed_Peas.txt', '2011-DJ_Got_Us_Fallin_In_Love-Usher.txt', '2012-Wild_Ones-Flo_Rida.txt',
                   '2010-I_Like_It-Enrique_Iglesias.txt', '2011-We_R_Who_We_R-Ke$ha.txt', '2014-Timber-Pitbull.txt', '2013-Beauty_And_A_Beat-Justin_Bieber.txt', '2011-Party_Rock_Anthem-LMFAO.txt', '2011-Till_The_World_Ends-Britney_Spears.txt', '2010-Bottoms_Up-Trey_Songz.txt', '2010-Say_Aah-Trey_Songz.txt', '2010-Dynamite-Taio_Cruz.txt',
                   '2010-Party_In_The_USA-Miley_Cyrus.txt', '2011-Give_Me_Everything-Pitbull.txt', '2012-Die_Young-Ke$ha.txt', '2015-Time_Of_Our_Lives-Pitbull.txt', '2011-Backseat-New_Boyz.txt', '2014-Birthday-Katy_Perry.txt']

queries = [query1, query2, query3]
relevant_queries = [query1_relevant, query2_relevant, query3_relevant]


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
    precision, recall, f1, tp, fp, fn = evaluate(matching_docs, relevant_queries[query_num-1])

    print("Evaluation")
    print(f"TP: {tp}")
    print(f"FP: {fp}")
    print(f"FN: {fn}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F-measure: {f1:.2f}")
