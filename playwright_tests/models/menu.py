'''Page Object Model for the Values Tracker side menu'''
class Menu:
    '''Menu object model class'''
    def __init__(self, page):
        self.page = page
        self.menu_button = page.locator('[data-testid="menuButton"]')
        self.home_button = page.locator('[data-testid="homeButton"]')
        self.manage_entities_button = page.locator(
            '[data-testid="manageEntitiesButton"]'
        )
        self.close_button = page.locator('[data-testid="closeButton"]')
        self.log_off_button = page.locator('[data-testid="logOffButton"]')
