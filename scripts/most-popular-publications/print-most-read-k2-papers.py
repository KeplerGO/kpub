import datetime
import kpub

def print_articles(articles):
    for idx, art in enumerate(articles):
        print("{}. {}\n{} ({})\n{} reads\n".format(idx+1,
                                                       art["title"][0].upper(),
                                                       art['first_author_norm'],
                                                       art['bibcode'],
                                                       art['read_count']))


if __name__ == "__main__":
    db = kpub.PublicationDB()
    articles = db.get_most_read(mission="k2", top=25)
    print("THE 25 MOST READ K2 PAPERS IN THE LAST 90 DAYS\n"
          "==============================================\n"
          "Last update: {}\n".format(datetime.datetime.now().strftime("%Y-%m-%d")))
    print_articles(articles)

