'''Page Object Model for Values Tracker Login Page'''
class LoginPage:
    '''Login page object model class'''
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator('[data-testid="usernameInput"]')
        self.password_input = page.locator('[data-testid="passwordInput"]')
        self.submit_button = page.locator('[data-testid="submitButton"]')
        self.register_button = page.locator('[data-testid="registerButton"]')
        self.error_message = page.locator('li[data-sonner-toast]')

    def login(self, username, password):
        '''
        Logs the provided user in
        Keyword arguments:
        username -- who to login
        password -- their password
        '''
        self.page.goto('http://localhost:3000/')
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()
