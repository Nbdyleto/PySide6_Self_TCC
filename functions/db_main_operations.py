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
            topic_name VARCHAR(255) NOT NULL,
            hits_percentage INTEGUER NOT NULL
        );"""
        self.cursor.execute(qry_topics)
        print('table topics is ready!')
    
    def popTblTopics(self, params):
        qry = "INSERT INTO topics (topic_id, topic_name, hits_percentage) VALUES (?,?,?);"
        self.cursor.execute(qry, (params))
        self.conn.commit()

    ###########################
    # Flashcards. DB Functions 

    def createTblFlashcards(self):
        # Child Table
        self.cursor.execute("DROP TABLE IF EXISTS flashcards")
        qry_flashcards = """ CREATE TABLE flashcards (
            card_question VARCHAR(255) NOT NULL,
            card_answer VARCHAR(255) NOT NULL,
            topic_id INTEGUER NOT NULL,
            FOREIGN KEY (topic_id)
                REFERENCES topics (topic_id)
            );"""
        self.cursor.execute(qry_flashcards)
        print('table flashcards is ready!')

    def popTblFlashcards(self, params):
        qry = "INSERT INTO flashcards (card_question, card_answer, topic_id) VALUES (?,?,?);"
        self.cursor.execute(qry, (params)) 
        self.conn.commit()
    
    def hasRecordsInTblFlashcards(self, id): 
        qry = f"SELECT COUNT(*) FROM flashcards WHERE (topic_id = ?)"
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
            task_name VARCHAR(255) NOT NULL, 
            status VARCHAR(255) NOT NULL,
            start_date DATE NOT NULL,
	        end_date DATE NOT NULL,	
            topic_id INTEGUER NOT NULL,
            FOREIGN KEY (topic_id)
            	REFERENCES topics (topic_id)
        );"""
        self.cursor.execute(qry_tasks)
        print('table tasks is ready!')

    def popTblTasks(self, params):
        qry = "INSERT INTO tasks VALUES (?,?,?,?,?);"
        self.cursor.execute(qry, (params))

    #########################
    # General. DB Functions

    def getRowCount(self, tbl):
        return self.cursor.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]

    def getAllRecords(self, tbl, specifcols='*', fetchall=True, whclause = None):
        if whclause is None:
            self.cursor.execute(f"SELECT {specifcols} FROM {tbl}")
        elif whclause is not None:
            self.cursor.execute(f"SELECT {specifcols} FROM {tbl} WHERE ({whclause})")    
        if fetchall:
            return self.cursor.fetchall()
        return self.cursor