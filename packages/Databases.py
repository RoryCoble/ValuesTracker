import psycopg2
from enum import Enum

class DatabaseConnector:
    def __init__(self, db_name, db_user, host, port):
        self.db_name = db_name
        self.db_user = db_user
        self.host = host
        self.port = port
        
    def __enter__(self):
        self.conn = psycopg2.connect(user = self.db_user,
                                     database = self.db_name,
                                     password = "data",
                                     host = self.host,
                                     port = self.port)
        return self.conn

    def __exit__(self, type, value, tb):
        self.conn.close()

class EntityOptions(Enum):
    SGFB = 'Slow Growth Fast Bust'
    V = 'Volatile'
    FD = 'Fluctuating Decline'
    FR = 'Fluctuating Rise'

class EntitiesValuesFunctions:
    def __init__(self, databaseConnection):
        self.conn = databaseConnection

    def get_existing_entities(self):
        entities = []
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('get_existing_entities')
                    entities = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return entities

    def add_entity(self, code, option, firstConstant, secondConstant, thirdConstant):
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('add_entity', (code, option, firstConstant, secondConstant, thirdConstant))
                    success = cur.fetchall()[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return success

    def add_entity_value(self, code, timestamp, value):
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('add_entity_value', (code, timestamp, value))
                    success = cur.fetchall()[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return success

    def get_entity_details(self, code):
        entityDetails = []
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('get_entity_details', (code,))
                    entityDetails = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return entityDetails

    def get_values(self, code, timestamp):
        values = []
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('get_values', (code, timestamp))
                    values = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return values