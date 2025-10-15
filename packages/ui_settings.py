'''SettingsState class'''
import os
import dataclasses

@dataclasses.dataclass
class SettingsState:
    """Static class to allow for the custom API used by the 
    frontend to be set by environment variable"""
    api_url = os.getenv('CUSTOM_API_URL', 'http://localhost:5001')
