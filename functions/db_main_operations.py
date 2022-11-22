import json
import sqlite3

#https://codereview.stackexchange.com/questions/182700/python-class-to-manage-a-table-in-sqlite
#https://blog.rtwilson.com/a-python-sqlite3-context-manager-gotcha/

class DBMainOperations:
    __DB_LOCATION = 'functions/db_main_operations.db'

    def __init__(self):
        self.conn = sqlite3.connect(DBMainOperations.__DB_LOCATION)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self
    
    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
    #"""
    
    ########################
    # Topics. DB Functions
    
    def createTblTopics(self):
        # Parent Table
        self.cursor.execute("DROP TABLE IF EXISTS topics")
        qry_topics = """ CREATE TABLE topics (
            topic_id INTEGUER PRIMARY KEY,
            topic_name VARCHAR(50) NOT NULL
        );"""
        self.cursor.execute(qry_topics)
        print('table topics is ready!')

    ###########################
    # Flashcards. DB Functions 

    def createTblDecks(self):
        # Parent Table of flashcards, Child Table of topics.
        self.cursor.execute("DROP TABLE IF EXISTS decks")
        qry_decks = """ CREATE TABLE decks (
            deck_id INTEGUER PRIMARY KEY,
            deck_name VARCHAR(50),
            hits_percentage INTEGUER NOT NULL,
            topic_id INTEGUER NOT NULL,
            FOREIGN KEY (topic_id)
                REFERENCES topics (topic_id)
        );"""
        self.cursor.execute(qry_decks)
        print('table decks is ready!')

    def createTblFlashcards(self):
        # Child Table
        self.cursor.execute("DROP TABLE IF EXISTS flashcards")
        qry_flashcards = """ CREATE TABLE flashcards (
            card_id INTEGUER PRIMARY KEY,
            card_question VARCHAR(255) NOT NULL,
            card_answer VARCHAR(255) NOT NULL,
            deck_id INTEGUER NOT NULL,
            FOREIGN KEY (deck_id)
                REFERENCES topics (deck_id)
            );"""
        self.cursor.execute(qry_flashcards)
        print('table flashcards is ready!')
    
    def hasRecordsInTblFlashcards(self, id): 
        qry = f"SELECT COUNT(*) FROM flashcards WHERE (deck_id = ?)"
        recordscount = self.cursor.execute(qry, str(id)).fetchall()[0][0]
        if recordscount > 0:
            return True
        return False

    ###########################
    # Daily Task. DB Functions

    def createTblTasks(self):
        # Child Table
        self.cursor.execute("DROP TABLE IF EXISTS tasks")
        qry_tasks = """ CREATE TABLE tasks (
            task_id INTEGUER PRIMARY KEY,
            task_name VARCHAR(255) NOT NULL, 
            status VARCHAR(25) NOT NULL,
            start_date DATE NOT NULL,
	        end_date DATE NOT NULL,	
            topic_id INTEGUER NOT NULL,
            FOREIGN KEY (topic_id)
            	REFERENCES topics (topic_id)
        );"""
        self.cursor.execute(qry_tasks)
        print('table tasks is ready!')

    ###########################
    # See Progress. DB Functions

    def createTblPomodoroProgress(self):
        # Child Table
        self.cursor.execute("DROP TABLE IF EXISTS pomodoroProgress")
        qry_pomoprogress = """ CREATE TABLE pomodoroProgress (
            pomo_id INTEGUER PRIMARY KEY,
            completed BOOL NOT NULL,
            study_date DATE NOT NULL,
            total_time TIME NOT NULL,
            topic_id INTEGUER NOT NULL,
            FOREIGN KEY (topic_id)
                REFERENCES topics (topic_id)
        );"""
        self.cursor.execute(qry_pomoprogress)
        print('table pomodoro progress ready!')

    #########################
    # General. DB Functions

    def populateTbl(self, tbl, params):
        qry = f"INSERT INTO {tbl} VALUES {params};"
        print(qry)
        self.cursor.execute(qry)
        self.conn.commit()

    def getRowCount(self, tbl, whclause=None):
        if whclause is None:
            return self.cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        return self.cursor.execute(f"SELECT COUNT(*) FROM {tbl} WHERE ({whclause})").fetchone()[0]

    def getAllRecords(self, tbl, specifcols='*', fetchall=True, whclause = None):
        if whclause is None:
            self.cursor.execute(f"SELECT {specifcols} FROM {tbl}")
        elif whclause is not None:
            self.cursor.execute(f"SELECT {specifcols} FROM {tbl} WHERE ({whclause})")    
        if fetchall:
            return self.cursor.fetchall()
        return self.cursor