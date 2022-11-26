from .db_main_operations import DBMainOperations
import json

class ImportExport:
    def __init__(self):
        pass

    def toJson(topicid, resetstats=True):
        """Convert a sqlite3 database to json based on Parent Table ID"""
        with DBMainOperations() as db:
            topicname = db.getAllRecords(tbl='topics', specifcols='topic_name', whclause=f'topic_id={topicid}')


            decks = db.getAllRecords(tbl='decks', fetchall=False, 
                                     whclause=f'topic_id={topicid}')
            decksrows = [row for row in decks]
            deckcols = [col[0] for col in decks.description]
        decks = []
        for row in decksrows:
            deck = {}
            for colname, val in zip(deckcols, row):
                deck[colname] = val 
            with DBMainOperations() as db:
                specifcols = 'card_question, card_answer'
                flashcards = db.getAllRecords(tbl='flashcards', specifcols=specifcols, 
                                              whclause=f'deck_id = {row[0]}')
                deck['flashcards'] = flashcards
            if resetstats:
                deck.pop('deck_id') 
                deck.pop('hits_percentage')
                deck.pop('bad_feedback')
                deck.pop('ok_feedback')
                deck.pop('good_feedback')
                deck.pop('topic_id')
            decks.append(deck)

        test = json.dumps(decks, indent=4)
        print(test)

        with open(f'functions/decks_of_{topicname[0][0].lower()}.json', 'w') as json_file:
            print(f"decks in JSON: {decks}")
            json.dump(decks, json_file, indent=4)

    def _to_mysql(self):
        """convert a json file to sqlite3 table"""
        pass

    