import psycopg2
from cryptography.fernet import Fernet

class UserFunctions:
    def __init__(self, databaseConnection):
        """Consumes the base databaseConnection and loads the encryption key used for User passwords"""
        self.conn = databaseConnection
        with self.conn:
            with self.conn.cursor() as cur:
                cur.callproc('get_encryption_key')
                self.key = cur.fetchall()[0][0]
        self.f = Fernet(self.key.encode())

    def add_user(self, userName, password, email):
        """
        Calls the stored function to add a new user
        Keyword arguments:
        userName -- string
        password -- string, encrypted by this function before being sent to the database
        email -- string
        """
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('add_user', (userName, self.f.encrypt(password.encode()).decode(), email))
                    success = cur.fetchall()[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return success

    def login_user(self, userName, password):
        """
        Calls the stored function to check that the provided information matches a registered User
        Keyword arguments:
        userName -- string
        password -- string
        """
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('get_user', (userName,))
                    response = cur.fetchall()[0]
                    if userName == response[0] and password == self.f.decrypt(response[1].encode()).decode():
                        success = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return success

    def get_entities_assigned_to_user(self, userName):
        """
        Gets the Entities connected to the provided User
        Keyword arguments:
        userName -- string
        """
        entities = []
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('get_entities_assigned_to_user', (userName,))
                    entities = cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return entities

    def connect_user_entity(self, userName, entityCode):
        """
        Connects the provided Entity to the provided User
        Keyword arguments:
        userName -- string
        entityCode -- string
        """
        success = False
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.callproc('connect_user_entity', (userName, entityCode))
                    success = cur.fetchall()[0][0]
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            return success