import reflex as rx
import os

class SettingsState:
    api_url = os.getenv('CUSTOM_API_URL', 'http://localhost:5001')