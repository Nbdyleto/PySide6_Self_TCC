from ..db_main_operations import DBMainOperations
import json

class ImportExport:
    def __init__(self):
        pass

    def _to_json(self, topic_id):
        """Convert a sqlite3 database to json"""
        with DBMainOperations() as db:
            decks = db.getAllRecords(tbl='decks', fetchall=False, whclause=f'topic_id={topic_id}')
            deck_rows = [row for row in decks]
            deck_cols = [col[0] for col in decks.description]
            
        decks = []
        for row in deck_rows:
            deck = {}
            for col_name, val in zip(deck_cols, row):
                deck[col_name] = val 
            with DBMainOperations() as db:
                flashcards = db.getAllRecords(tbl='flashcards', whclause=f'deck_id = {row[0]}')
                deck['flashcards'] = flashcards
            decks.append(deck)

        test = json.dumps(decks, indent=4)
        print(test)

        with open('functions/flashcards/decksJSON.json', 'w') as json_file:
            print(f"decks in JSON: {decks}")
            json.dump(decks, json_file, indent=4)
    
    def _to_mysql(self):
        """convert a json file to sqlite3 table"""
        pass
