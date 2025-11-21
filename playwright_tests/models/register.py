'''Page Object Model for the Values Tracker Register page'''
class RegisterPage:
    '''Register page object model class'''
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator('[data-testid="usernameInput"]')
        self.password_input = page.locator('[data-testid="passwordInput"]')
        self.email_input = page.locator('[data-testid="emailInput"]')
        self.submit_button = page.locator('[data-testid="submitButton"]')
        self.cancel_button = page.locator('[data-testid="cancelButton"]')

    def register_user(self, username, password, email):
        '''
        Registers a user through the UI
        Keyword arguments:
        username -- desired username to be created
        password -- related password string
        email -- email address for created user
        '''
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.email_input.fill(email)
        self.submit_button.click()
