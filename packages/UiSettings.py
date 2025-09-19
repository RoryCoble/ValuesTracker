import reflex as rx
import os

class SettingsState:
    api_url = os.getenv('api_url', 'http://localhost:5001')