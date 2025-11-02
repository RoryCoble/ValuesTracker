'''SettingsState class'''
import os
import dataclasses

@dataclasses.dataclass
class SettingsState:
    """Static class to allow for the custom API used by the 
    frontend to be set by environment variable"""
    api_url = os.getenv('CUSTOM_API_URL', 'http://localhost:5001')
    color_list = ['#79bf24','#24aabf','#bf2453',
                  '#9eb7ff','#e59eff','#ff9eab',
                  '#f2ff9e','#9effc2','#ff9e9e',
                  '#ffd59e']
