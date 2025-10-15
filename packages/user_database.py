'''Methods to interact with the stored User functions in the database'''
import psycopg2
from cryptography.fernet import Fernet

class UserFunctions:
    '''Class for User functions in the database'''
    def __init__(self, database_connection):
        """Consumes the base databaseConnection and loads the encryption 
        key used for User passwords"""
        self.conn = database_connection
        with self.conn:
            with self.conn.cursor() as cur:
                cur.callproc('get_encryption_key')
                self.key = cur.fetchall()[0][0]
        self.f = Fernet(self.key.encode())

    def add_user(self, user_name, password, email):
        """
        Calls the stored function to add a new user
        Keyword arguments:
        user_name -- string
        password -- string, encrypted by this function before being sent to the database
        email -- string
        """
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('add_user',
                                 (user_name, self.f.encrypt(password.encode()).decode(), email))
                    success = cur.fetchall()[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return success

    def login_user(self, user_name, password):
        """
        Calls the stored function to check that the provided information matches a registered User
        Keyword arguments:
        user_name -- string
        password -- string
        """
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('get_user', (user_name,))
                    response = cur.fetchall()[0]
                    # pylint: disable=line-too-long
                    if user_name == response[0] and password == self.f.decrypt(response[1].encode()).decode():
                        success = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return success

    def get_entities_assigned_to_user(self, user_name):
        """
        Gets the Entities connected to the provided User
        Keyword arguments:
        user_name -- string
        """
        entities = []
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('get_entities_assigned_to_user', (user_name,))
                    entities = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return entities

    def connect_user_entity(self, user_name, entity_code):
        """
        Connects the provided Entity to the provided User
        Keyword arguments:
        user_name -- string
        entity_code -- string
        """
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('connect_user_entity', (user_name, entity_code))
                    success = cur.fetchall()[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return success
