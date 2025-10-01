import requests as rq

class ApiRequests:
    """Wrapper class for the custom API consumed by the frontend"""
    def __init__(self, basePath):
        self.basePath = basePath

    def get_entities(self):
        """Gets all of the currently existing Entities"""
        return rq.get(f"{self.basePath}/api/get_existing_entities")

    def get_historical_values(self, entityCode):
        """
        Gets all of the values for the given Entity up to the moment of calling
        Keyword arguments:
        entityCode -- code for the Entity whose historical values are being gotten
        """
        return rq.get(f"{self.basePath}/api/get_historical_values?code={entityCode}")

    def get_new_values(self, entityCode, timestamp):
        """
        Gets all of the values for the given Entity from the provided timestamp up to the moment of calling
        Keyword arguments:
        entityCode -- code for the Entity whose values are being gotten
        timestamp -- time for which Values occuring at or after are returned
        """
        return rq.get(f"{self.basePath}/api/get_new_values?code={entityCode}&timestamp={timestamp}")

    def create_user(self, userName, password, email):
        """
        Posts the provided information to create a new user
        Keyword arguments:
        userName -- string
        password -- string
        email -- string
        """
        response = rq.post(f"{self.basePath}/api/create_user", data = {
            "userName" : userName,
            "password" : password,
            "email"    : email
        })
        if response.json() == False:
            raise Exception("User failed to be created")
        return response
        
    def login_user(self, userName, password):
        """
        Post to confirm that the provided user name and password
        """
        return rq.post(f"{self.basePath}/api/login_user", data = {
            "userName" : userName,
            "password" : password
        })

    def connect_user_entity(self, userName, entityCode):
        return rq.post(f"{self.basePath}/api/connect_user_entity", data = {
            "userName"   : userName,
            "entityCode" : entityCode
        })

    def get_entities_assigned_to_user(self, userName):
        return rq.get(f"{self.basePath}/api/get_entities_assigned_to_user?userName={userName}")

    def get_entity_details(self, code):
        return rq.get(f"{self.basePath}/api/get_entity_details?code={code}")