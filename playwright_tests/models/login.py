'''Page Object Model for Values Tracker Login Page'''
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator('[data-testid="usernameInput"]')
        self.password_input = page.locator('[data-testid="passwordInput"]')
        self.submit_button = page.locator('[data-testid="submitButton"]')
        self.register_link = page.locator('[data-testid="registerLink"]')

    def login(self, username, password):
        self.page.goto('http://localhost:3000/')
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()