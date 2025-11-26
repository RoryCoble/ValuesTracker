'''Page Object Model for Values Tracker Manage Entities Page'''
class ManageEntitiesPage:
    '''Main Entities page object model class'''
    def __init__(self, page):
        self.page = page
        self.code_header = page.locator('[data-testid="codeHeader"]')
        self.type_header = page.locator('[data-testid="typeHeader"]')
        self.first_constant_header = page.locator('[data-testid="firstConstantHeader"]')
        self.second_constant_header = page.locator('[data-testid="secondConstantHeader"]')
        self.third_constant_header = page.locator('[data-testid="thirdConstantHeader"]')
        self.add_entity_button = page.locator('[data-testid="addEntityButton"]')
        self.add_entity_options = page.locator('[data-testid="entitySelect"]')
        self.entity_select_options = page.locator('select[name="entity"] option')
        self.entity_select = page.locator('select[name="entity"]')

    def get_entity_row_value_by_location(self, location):
        '''
        Abstracts the row values by location
        Keyword arguments:
        location -- integer representing where the element 
                    falls in the list of row values
        '''
        return self.page.locator('[data-testid="entitiesTableRow"] td').nth(location)
