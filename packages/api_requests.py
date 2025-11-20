'''Api Requests class'''
import pandas as pd
import requests as rq

class ApiRequests:
    """Wrapper class for the custom API consumed by the frontend"""
    def __init__(self, base_path):
        self.base_path = base_path

    def get_entities(self):
        """Gets all of the currently existing Entities"""
        print(self.base_path)
        return rq.get(f"{self.base_path}/api/get_existing_entities", timeout=10)

    def get_historical_values(self, entity_code):
        """
        Gets all of the values for the given Entity up to the moment of calling
        Keyword arguments:
        entity_code -- code for the Entity whose historical values are being gotten
        """
        return rq.get(f"{self.base_path}/api/get_historical_values?code={entity_code}", timeout=10)

    def get_new_values(self, entity_code, count):
        """
        Gets all of the values for the given Entity from the provided 
        timestamp up to the moment of calling
        Keyword arguments:
        entity_code -- code for the Entity whose values are being gotten
        count -- time for which Values occuring at or after are returned
        """
        return rq.get(f"{self.base_path}/api/get_new_values?"
                      + f"code={entity_code}&count={count}", timeout=10)

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

    def get_collected_graph_data(self, entities):
        """
        Collects the values data and wraps it up for the multiple graphs
        Keyword arguments:
        entities -- list of entities assigned to user
        """
        collected_graph_data = []
        for entity in entities:
            response = self.get_historical_values(entity).json()
            collected_graph_data.append(response)
        if not collected_graph_data:
            last_count = None
        else:
            last_count = collected_graph_data[-1][-1]['count']

        return (last_count, collected_graph_data)

    def extend_collected_graph_data(self, collected_graph_data, entities, count):
        """
        Gets new values and appends them to the collected
        graph data for the related entity
        Keyword arguments:
        collected_graph_data -- current dataset for the Entity based graphs
        entities -- list of Entities assigned to the user
        """
        i=0
        for entity in entities:
            new_data = self.get_new_values(entity,
                                           count).json()
            collected_graph_data[i].extend(new_data)
            collected_graph_data[i] = pd.DataFrame(
                collected_graph_data[i]).drop_duplicates().sort_values(
                by="count").to_dict(orient='records')
            i+=1

        if not collected_graph_data:
            last_count = count
        else:
            last_count = collected_graph_data[-1][-1]['count']

        return (last_count, collected_graph_data)

    def get_data_for_totals_chart(self, collected_graph_data, entities):
        """
        Takes the current collected graph data and assembles it in the
        way Reflex wants to see multiple lines on a chart
        Keywords arguments:
        collected_graph_data -- current dataset for the Entity based graphs
        entities -- list of Entities assigned to the user
        """
        i=0
        df = pd.DataFrame()
        for entity in entities:
            if i == 0:
                df = pd.DataFrame(collected_graph_data[i])
                df = df.rename(columns={'value':entity})
            else:
                df2 = pd.DataFrame(collected_graph_data[i])
                df = df.merge(df2,
                              how='outer', 
                              on='count'
                             ).rename(
                    columns={'value':entity})
            i+=1
        return df.to_dict(orient='records')
