import psycopg2
from cryptography.fernet import Fernet

class UserFunctions:
    def __init__(self, databaseConnection):
        self.conn = databaseConnection
        with self.conn:
            with self.conn.cursor() as cur:
                cur.callproc('get_encryption_key')
                self.key = cur.fetchall()[0][0]
        self.f = Fernet(self.key.encode())

    def add_user(self, userName, password, email):
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