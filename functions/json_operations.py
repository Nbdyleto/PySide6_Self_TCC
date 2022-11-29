from .db_main_operations import DBMainOperations
import json

class ImportExport:
    def __init__(self):
        pass

    def toJson(topicid, resetstats=True):
        """Convert a sqlite3 database to json based on Parent Table ID"""
        with DBMainOperations() as db:
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
                topicname = db.getAllRecords(tbl='topics', specifcols='topic_name', 
                                             whclause=f'topic_id={topicid}')
                specifcols = 'card_question, card_answer'
                flashcards = db.getAllRecords(tbl='flashcards', specifcols=specifcols, 
                                              whclause=f'deck_id = {row[0]}')
                deck['topic_name'] = topicname[0][0]
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

        with open(f'functions/decks.json', 'w') as json_file:
            print(f"decks in JSON: {decks}")
            json.dump(decks, json_file, indent=4)

    def toSQLite3(file=None):
        """convert a json file to sqlite3 table"""
        data = json.load(open('functions/decks.json'))
        for row in data:
            deckname = row['deck_name']
            topicname = row['topic_name']
            with DBMainOperations() as db:
                ################
                # verify the existence of topic in DB, if exists, not add.
                exists = db.cursor.execute(f"""
                    SELECT EXISTS(SELECT 1 FROM topics WHERE topic_name="{topicname}");"""
                ).fetchall()[0][0]
                if exists == 0: # not existent, so, populate tbl topics.
                    qry = 'SELECT * FROM topics ORDER BY topic_id DESC LIMIT 1;'
                    lastTopicID = activeTopicID = db.cursor.execute(qry).fetchall()[0][0]+1
                    db.populateTbl(tbl='topics', params=(activeTopicID, topicname))
                else:
                    activeTopicID = db.getAllRecords(tbl='topics', specifcols='topic_id', 
                                                     whclause=f'topic_name = "{topicname}"')[0][0]
                
                ################
                # verify the existence of deck in DB, if exists, not add.
                exists = db.cursor.execute(f"""
                    SELECT EXISTS(SELECT 1 FROM decks WHERE deck_name="{deckname}");"""
                ).fetchall()[0][0]
                if exists == 0: # not existent, so, populate tbl topics.
                    qry = 'SELECT * FROM decks ORDER BY deck_id DESC LIMIT 1;'

                    exist = db.cursor.execute(f"""
                        SELECT EXISTS(SELECT 1 FROM decks);"""
                    ).fetchall()[0][0]
                    existAtLeastADeck = True if exist == 1 else False
                    print('existAtLeastADeck:', existAtLeastADeck)
                    if existAtLeastADeck:
                        lastDeckID = activeDeckID = db.cursor.execute(qry).fetchall()[0][0]+1
                    else:
                        lastDeckID = activeDeckID = 0

                    db.populateTbl(tbl='decks', params=(activeDeckID, deckname, 0, 0, 0, 0, activeTopicID))
                else:
                    activeDeckID = db.getAllRecords(tbl='decks', specifcols='deck_id', 
                                                    whclause=f'deck_name = "{deckname}"')[0][0]
            
                for flashcard in row['flashcards']:
                    question, answer = flashcard[0], flashcard[1]
                    qry = 'SELECT * FROM flashcards ORDER BY card_id DESC LIMIT 1;'
                    lastCardID = db.cursor.execute(qry).fetchall()[0][0]+1
                    print('ADDING CARDS: ', lastCardID, question, answer, activeDeckID)
                    db.populateTbl(tbl='flashcards', params=(lastCardID, question, answer, activeDeckID))

    