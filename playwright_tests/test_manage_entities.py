'''Tests the Manage Entities UI'''
import re
import pytest
from playwright.sync_api import sync_playwright, expect
from tests.setup_functions import SetupFunctions
from .models.login import LoginPage
from .models.all import AllPage
from .models.menu import Menu
from .models.manage_entities import ManageEntitiesPage

@pytest.fixture(scope='class', name='setup')
def fixture_setup():
    """Creates the expected test data, renders the browser page, 
    then cleans up any added data after the tests have run"""
    SetupFunctions().truncate_entities()
    SetupFunctions().truncate_users()

    # Create and attach user here
    with sync_playwright() as playwright:
        page = playwright.webkit.launch().new_context().new_page()
        all_page = AllPage(page)
        all_page.create_user('a','a','a')
        all_page.add_entity('AAAAA', 'Volatile', 7.2)
        LoginPage(page).login('a','a')
        menu = Menu(page)
        menu.menu_button.click()
        menu.manage_entities_button.click()

        yield (ManageEntitiesPage(page), all_page)

    SetupFunctions().truncate_users()
    SetupFunctions().truncate_entities()

def test_code_header_displays(setup):
    '''Tests that the Code table header displays'''
    (manage_entities, _) = setup
    expect(
        manage_entities.code_header,
        "Code header is not displayed"
    ).to_be_visible()
    expect(
        manage_entities.code_header,
        "Code header text is incorrect"
    ).to_contain_text("Code")

def test_type_header_displays(setup):
    '''Tests that the Type table header displays'''
    (manage_entities, _) = setup
    expect(
        manage_entities.type_header,
        "Type header is not displayed"
    ).to_be_visible()
    expect(
        manage_entities.type_header,
        "Type header text is incorrect"
    ).to_contain_text("Type")

def test_first_constant_header_displays(setup):
    '''Tests that the First Constant header displays'''
    (manage_entities, _) = setup
    expect(
        manage_entities.first_constant_header,
        "First Constant header is not displayed"
    ).to_be_visible()
    expect(
        manage_entities.first_constant_header,
        "First Constant header text is incorrect"
    ).to_contain_text("First Constant")

def test_second_constant_header_displays(setup):
    '''Tests that the Second Constant header displays'''
    (manage_entities, _) = setup
    expect(
        manage_entities.second_constant_header,
        "Second Constant header is not displayed"
    ).to_be_visible()
    expect(
        manage_entities.second_constant_header,
        "Second Constant header text is incorrect"
    ).to_contain_text("Second Constant")

def test_third_constant_header_displays(setup):
    '''Tests that the Third Constant header displays'''
    (manage_entities, _) = setup
    expect(
        manage_entities.third_constant_header,
        "Third Constant header is not displayed"
    ).to_be_visible()
    expect(
        manage_entities.third_constant_header,
        "Third Constant header text is incorrect"
    ).to_contain_text("Third Constant")

def test_entity_select_has_the_expected_values(setup):
    '''Tests that the Entity select has the expected values'''
    (manage_entities, _) = setup
    expect(
        manage_entities.add_entity_options,
        "Entity Options select is not displayed"
    ).to_be_visible()
    manage_entities.add_entity_options.click()
    expect(
        manage_entities.entity_select_options,
        "Entity Options are as expected"
    ).to_have_text(["AAAAA", "Select Entity"])

def test_add_entity_button_displays(setup):
    '''Tests that the Add Entity button is displayed'''
    (manage_entities, _) = setup
    expect(
        manage_entities.add_entity_button,
        "Add Entity button is not displayed"
    ).to_be_visible()
    expect(
        manage_entities.add_entity_button,
        "Add Entity button text is incorrect"
    ).to_contain_text("Add Entity")

def test_entities_can_be_added(setup):
    '''Tests that a user can add an Entity'''
    (manage_entities, _) = setup
    manage_entities.add_entity_options.click()
    manage_entities.entity_select.select_option('AAAAA')
    manage_entities.add_entity_button.click()
    expect(
        manage_entities.get_entity_row_value_by_location(0)
    ).to_contain_text("AAAAA")
    expect(
        manage_entities.get_entity_row_value_by_location(1)
    ).to_contain_text("Volatile")
    expect(
        manage_entities.get_entity_row_value_by_location(2)
    ).to_contain_text("7.2")
    expect(
        manage_entities.get_entity_row_value_by_location(3)
    ).to_contain_text("7.2")
    expect(
        manage_entities.get_entity_row_value_by_location(4)
    ).to_contain_text("7.2")
