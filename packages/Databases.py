import psycopg2
from enum import Enum

class DatabaseConnector:
    """Generalized Database connection wrapper class"""
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
    """Kinds of Entities that can be generated"""
    SGFB = 'Slow Growth Fast Bust'
    V = 'Volatile'
    FD = 'Fluctuating Decline'
    FR = 'Fluctuating Rise'

class EntitiesValuesFunctions:
    """Custom functions allowing for Entities & Values data manipulation"""
    def __init__(self, databaseConnection):
        self.conn = databaseConnection

    def get_existing_entities(self):
        """Retrieves all of the currently available Entities"""
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
        """
        Creates a new Entity in the database
        Keyword arguments:
        code -- the desired Entity Code string
        option -- value from the EntityOptions enum
        firstConstant -- decimal used during calculation of values generated for this entity
        secondConstant -- decimal used during calculation of values generated for this entity
        thirdConstant -- decimal used during calculation of values generated for this entity
        """
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
        """
        Adds the provided Value for a given Entity
        Keyword arguments:
        code -- the code for the Entity that the Value will be attached to
        timestamp -- when the Entity had the provided Value
        value -- numeric entry for the provided Entity
        """
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
        """
        Gets the provided Entities type and constants
        Keyword arguments:
        code -- the Entity whose details will be returned
        """
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
        """
        Gets the Values connected to the provided Entity that occurred after the provided timestamp
        Keyword arguments:
        code -- Entity that has the requested values
        timestamp -- all values returned are after this timestamp
        """
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