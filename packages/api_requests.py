'''Api Requests class'''
import requests as rq

class ApiRequests:
    """Wrapper class for the custom API consumed by the frontend"""
    def __init__(self, base_path):
        self.base_path = base_path

    def get_entities(self):
        """Gets all of the currently existing Entities"""
        return rq.get(f"{self.base_path}/api/get_existing_entities", timeout=10)

    def get_historical_values(self, entity_code):
        """
        Gets all of the values for the given Entity up to the moment of calling
        Keyword arguments:
        entity_code -- code for the Entity whose historical values are being gotten
        """
        return rq.get(f"{self.base_path}/api/get_historical_values?code={entity_code}", timeout=10)

    def get_new_values(self, entity_code, timestamp):
        """
        Gets all of the values for the given Entity from the provided 
        timestamp up to the moment of calling
        Keyword arguments:
        entity_code -- code for the Entity whose values are being gotten
        timestamp -- time for which Values occuring at or after are returned
        """
        return rq.get(f"{self.base_path}/api/get_new_values?"
                      + f"code={entity_code}&timestamp={timestamp}", timeout=10)

    def create_user(self, user_name, password, email):
        """
        Posts the provided information to create a new user
        Keyword arguments:
        user_name -- string
        password -- string
        email -- string
        """
        response = rq.post(f"{self.base_path}/api/create_user", data = {
            "userName" : user_name,
            "password" : password,
            "email"    : email
        }, timeout=10)
        if response.json() is False:
            raise Exception("User failed to be created")
        return response

    def login_user(self, user_name, password):
        """
        Post to confirm that the provided user name and password
        Keyword arguments:
        user_name -- string
        password -- string
        """
        return rq.post(f"{self.base_path}/api/login_user", data = {
            "userName" : user_name,
            "password" : password
        }, timeout=10)

    def connect_user_entity(self, user_name, entity_code):
        """
        Post to assign the provided Entity to the provided User
        Keyword arguments:
        user_name -- string
        entity_code -- string
        """
        return rq.post(f"{self.base_path}/api/connect_user_entity", data = {
            "userName"   : user_name,
            "entityCode" : entity_code
        }, timeout=10)

    def get_entities_assigned_to_user(self, user_name):
        """
        Get the Entities assigned to the provided User
        Keyword arguments:
        user_name -- string
        """
        return rq.get(f"{self.base_path}/api/get_entities_assigned_to_user" +
                      f"?userName={user_name}", timeout=10)

    def get_entity_details(self, code):
        """
        Get the Details of the provided Entity
        Keyword arguments:
        code -- string
        """
        return rq.get(f"{self.base_path}/api/get_entity_details?code={code}", timeout=10)
