from db_flashcards_operations import FlashcardsDB
import json

class ImportExport:
    def __init__(self):
        pass

    def _to_json(self):
        """Convert a sqlite3 database to json"""
        with FlashcardsDB() as db:
            results = db.cursor.execute("SELECT * from topics")
            rows = [row for row in results]
            cols = [col for col in results.description]

        topics = []
        for row in rows:
            topic = {}
            for col_name, val in zip(cols, row):
                topic[col_name] = val
            topics.append(row)
            
        with open('functions/flashcards/topics.json', 'w') as json_file:
            topicsJSON = json.dumps(topics, indent=4)
            print(f"topics in JSON: {topicsJSON}")
            json.dump(topicsJSON, json_file)
    
    def _to_mysql(self):
        """convert a json file to sqlite3 table"""
        pass
