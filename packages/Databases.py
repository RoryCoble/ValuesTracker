'''General functions for the non-User database interactions'''
from enum import Enum
import psycopg2

class DatabaseConnector:
    """Generalized Database connection wrapper class"""
    def __init__(self, db_name, db_user, host, port):
        self.db_name = db_name
        self.db_user = db_user
        self.host = host
        self.port = port
        self.conn = object

    def __enter__(self):
        self.conn = psycopg2.connect(user = self.db_user,
                                     database = self.db_name,
                                     password = "data",
                                     host = self.host,
                                     port = self.port)
        return self.conn

    def __exit__(self, fixture_type, value, tb):
        self.conn.close()

class EntityOptions(Enum):
    """Kinds of Entities that can be generated"""
    SGFB = 'Slow Growth Fast Bust'
    V = 'Volatile'
    FD = 'Fluctuating Decline'
    FR = 'Fluctuating Rise'

class EntitiesValuesFunctions:
    """Custom functions allowing for Entities & Values data manipulation"""
    def __init__(self, database_connection):
        self.conn = database_connection

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

        return entities

    def add_entity(self, code, option, first_constant, second_constant, third_constant):
        """
        Creates a new Entity in the database
        Keyword arguments:
        code -- the desired Entity Code string
        option -- value from the EntityOptions enum
        first_constant -- decimal used during calculation of values generated for this entity
        second_constant -- decimal used during calculation of values generated for this entity
        third_constant -- decimal used during calculation of values generated for this entity
        """
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('add_entity',
                                 (code, option, first_constant, second_constant, third_constant))
                    success = cur.fetchall()[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return success

    def add_entity_value(self, code, count, value):
        """
        Adds the provided Value for a given Entity
        Keyword arguments:
        code -- the code for the Entity that the Value will be attached to
        count -- when the Entity had the provided Value
        value -- numeric entry for the provided Entity
        """
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('add_entity_value', (code, count, value))
                    success = cur.fetchall()[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return success

    def get_entity_details(self, code):
        """
        Gets the provided Entities type and constants
        Keyword arguments:
        code -- the Entity whose details will be returned
        """
        entity_details = []
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('get_entity_details', (code,))
                    entity_details = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return entity_details

    def get_values(self, code, count):
        """
        Gets the Values connected to the provided Entity that occurred after the provided timestamp
        Keyword arguments:
        code -- Entity that has the requested values
        count -- all values returned are after this count
        """
        values = []
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('get_values', (code, count))
                    values = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return values
