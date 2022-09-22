from ..db_main_operations import DBMainOperations
import json

class ImportExport:
    def __init__(self):
        pass

    def _to_json(self):
        """Convert a sqlite3 database to json"""
        with DBMainOperations() as db:
            decks = db.getAllRecords(tbl='decks', fetchall=False)
            rows = [row for row in decks]
            cols = [col[0] for col in decks.description]
        print(rows)

        decks = []
        for row in rows:
            deck = {}
            for col_name, val in zip(cols, row):
                deck[col_name] = val
            decks.append(deck)
            
        with open('functions/flashcards/decksJSON.json', 'w') as json_file:
            print(f"decks in JSON: {decks}")
            json.dump(decks, json_file, indent=4)
    
    def _to_mysql(self):
        """convert a json file to sqlite3 table"""
        pass
