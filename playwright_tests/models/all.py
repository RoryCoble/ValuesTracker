'''Page Object Model for Values Tracker Pages in general'''
import os
import requests as rq
from playwright.sync_api import expect

class AllPage:
    '''General page object model class'''
    def __init__(self, page):
        self.page = page
        self.page_title = page.locator('[data-testid="pageTitle"]')
        self.api_url = os.getenv('CUSTOM_API_URL', 'http://localhost:5001')
        self.dataseeder_api_url = os.getenv('DATASEEDER_URL', 'http://localhost:5002')

    def create_user(self, username, password, email):
        '''
        Creates a user
        Keyword arguments:
        username -- desired username to be created
        password -- related password string
        email -- email address for created user
        '''
        data = {
            'userName': username,
            'password': password,
            'email': email
        }
        _ = rq.post(f"{self.api_url}/api/create_user", data = data, timeout=10)

    def connect_user_entity(self, username, entity):
        '''
        Connects a given user to the given entity
        Keyword arguments:
        username -- user to connect the entity to
        entity -- entity to be connected
        '''
        data = {
            'userName': username,
            'entityCode': entity
        }
        _ = rq.post(f"{self.api_url}/api/connect_user_entity", data = data, timeout=10)

    def add_entity(self, entity, entity_type, constant):
        '''
        Adds an entity for connection
        Keyword arguments:
        entity -- code used to label the entity
        entity_type -- type of entity
        constant -- numeric value used for calculations
        '''
        data = {
            'entityCode': entity,
            'entityType': entity_type, 
            'firstConstant': constant,
            'secondConstant': constant, 
            'thirdConstant': constant
        }
        _ = rq.post(f"{self.dataseeder_api_url}/dataseed/add_entity", data = data, timeout=10)

    def generate_value(self, count, entity):
        '''
        Generates a value for a given Entity
        Keyword arguments:
        count -- numeric value used in calculations
        entity -- entity to add a value to
        '''
        data = {
            'count': count,
            'entityCode': entity
        }
        return rq.post(f"{self.dataseeder_api_url}/dataseed/add_value", data = data, timeout=10)

    def test_page_title(self, page_title):
        '''
        Abstracts the testing of each pages title
        since they all share IDs
        Keyword arguments:
        page_title -- string of the expected Page Title
        '''
        expect(
            self.page_title,
            "Page title is not displayed"
        ).to_be_visible()
        expect(
            self.page_title,
            "Page title text does not match"
        ).to_contain_text(page_title)
