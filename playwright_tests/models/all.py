'''Page Object Model for Values Tracker Pages in general'''
import os
import requests as rq
from playwright.sync_api import Page

class AllPage:
    def __init__(self, page):
        self.page = page
        self.page_title = page.locator('[data-testid="pageTitle"]')
        self.api_url = os.getenv('CUSTOM_API_URL', 'http://localhost:5001')
        self.dataseeder_api_url = os.getenv('DATASEEDER_URL', 'http://localhost:5002')

    def create_user(self, username, password, email):
        data = {
            'userName': username,
            'password': password,
            'email': email
        }
        _ = rq.post(f"{self.api_url}/api/create_user", data = data, timeout=10)

    def connect_user_entity(self, username, entity):
        data = {
            'userName': username,
            'entityCode': entity
        }
        _ = rq.post(f"{self.api_url}/api/connect_user_entity", data = data, timeout=10)

    def add_entity(self, entity, entity_type, constant):
        data = {
            'entityCode': entity,
            'entityType': entity_type, 
            'firstConstant': constant,
            'secondConstant': constant, 
            'thirdConstant': constant
        }
        _ = rq.post(f"{self.dataseeder_api_url}/dataseed/add_entity", data = data, timeout=10)

    def generate_value(self, count, entity):
        data = {
            'count': count,
            'entityCode': entity
        }
        return rq.post(f"{self.dataseeder_api_url}/dataseed/add_value", data = data, timeout=10)
