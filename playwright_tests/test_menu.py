'''Tests the menu UI'''
import re
import pytest
from playwright.sync_api import sync_playwright, expect
from tests.setup_functions import SetupFunctions
from .models.login import LoginPage
from .models.all import AllPage
from .models.menu import Menu

@pytest.fixture(scope='class', name='setup')
def fixture_setup():
    """Creates the expected test data, renders the browser page, 
    then cleans up any added data after the tests have run"""
    SetupFunctions().truncate_entities()
    SetupFunctions().truncate_users()

    # Create and attach user here
    with sync_playwright() as playwright:
        page = playwright.webkit.launch().new_context().new_page()
        AllPage(page).create_user('a','a','a')
        LoginPage(page).login('a','a')
        menu = Menu(page)
        menu.menu_button.click()
        yield menu

    SetupFunctions().truncate_users()
    SetupFunctions().truncate_entities()

def tests_home_button_displays(setup):
    '''Tests that the menu's home button displays'''
    expect(
        setup.home_button,
        "Home button does not display"
    ).to_be_visible()
    expect(
        setup.home_button,
        "Home button is not disabled"
    ).to_be_disabled()
    expect(
        setup.home_button,
        "Home button text is not correct"
    ).to_contain_text("Home")

def tests_manage_entities_button_displays(setup):
    '''Tests that the menu's manage entities button displays'''
    expect(
        setup.manage_entities_button,
        "Manage Entities button does not display"
    ).to_be_visible()
    expect(
        setup.manage_entities_button,
        "Manage Entities button is not enabled"
    ).not_to_be_disabled()
    expect(
        setup.manage_entities_button,
        "Manage Entities button text is not correct"
    ).to_contain_text("Manage Entities")

def tests_log_off_button_displays(setup):
    '''Tests that the menu's Log Off button displays'''
    expect(
        setup.log_off_button,
        "Log Off button does not display"
    ).to_be_visible()
    expect(
        setup.log_off_button,
        "Log Off button is not enabled"
    ).not_to_be_disabled()
    expect(
        setup.log_off_button,
        "Log Off button text is not correct"
    ).to_contain_text("Log Off")

def tests_close_button_displays(setup):
    '''Tests that the menu's Close button displays'''
    expect(
        setup.close_button,
        "Close button does not display"
    ).to_be_visible()
    expect(
        setup.close_button,
        "Close button is not enabled"
    ).not_to_be_disabled()
    expect(
        setup.close_button,
        "Close button text is not correct"
    ).to_contain_text("Close")

def tests_navigation_to_manage_entities(setup):
    '''Tests that the user can navigate to the Manage Entities page'''
    setup.manage_entities_button.click()
    expect(setup.page).to_have_url(re.compile("/entities"))
    setup.menu_button.click()
    expect(
        setup.home_button,
        "Home button is not enabled"
    ).not_to_be_disabled()
    expect(
        setup.manage_entities_button,
        "Manage Entities button is not disabled"
    ).to_be_disabled()

def tests_menu_closes_when_button_is_clicked(setup):
    '''Tests that the menu closes when the close button is clicked'''
    setup.close_button.click()
    expect(
        setup.close_button,
        "Menu hasn't closed"
    ).to_be_hidden()

def tests_user_can_log_off(setup):
    '''Tests that a user clicking the log off button logs them off'''
    setup.log_off_button.click()
    expect(setup.page).to_have_url(re.compile("/login"))
