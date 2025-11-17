'''Tests the Login page UI'''
import pytest
from playwright.sync_api import sync_playwright, expect
from tests.setup_functions import SetupFunctions
from .models.login import LoginPage
from .models.all import AllPage

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
        page.goto('http://localhost:3000/')
        yield (LoginPage(page), all_page)

    SetupFunctions().truncate_users()
    SetupFunctions().truncate_entities()

def test_login_page_title_displays(setup):
    '''Tests that the page title on the Login page displays'''
    (_, all_page) = setup
    all_page.test_page_title('Login')

def test_login_page_username_input_displays(setup):
    '''Tests that the username input on the Login page displays'''
    (login_page, _) = setup
    expect(
        login_page.username_input,
        "Username input is not displayed"
    ).to_be_visible()
    expect(
        login_page.username_input,
        "Username placeholder is not correct"
    ).to_have_attribute("placeholder", "User Name")

def test_login_page_password_input_displays(setup):
    '''Tests that the password input on the Login page displays'''
    (login_page, _) = setup
    expect(
        login_page.password_input,
        "Password input is not displayed"
    ).to_be_visible()
    expect(
        login_page.password_input,
        "Password placeholder is not correct"
    ).to_have_attribute("placeholder", "Password")

def test_login_page_submit_button_displays(setup):
    '''Tests that the submit button on the Login page displays'''
    (login_page, _) = setup
    expect(
        login_page.submit_button,
        "Submit button is not displayed"
    ).to_be_visible()
    expect(
        login_page.submit_button,
        "Submit button text is not correct"
    ).to_contain_text("Submit")

def test_login_page_register_link_displays(setup):
    '''Tests that the register link on the Login page displays'''
    (login_page, _) = setup
    expect(
        login_page.register_link,
        "Register link is not displayed"
    ).to_be_visible()
    expect(
        login_page.register_link,
        "Register link text is not correct"
    ).to_contain_text("Register")

def test_login_successful(setup):
    '''Tests that a registered user can log in'''
    (login_page, all_page) = setup
    login_page.login('a','a')
    expect(
        all_page.page_title,
        "Page title is not displayed"
    ).to_be_visible()
    expect(
        all_page.page_title,
        "Page title text does not match"
    ).to_contain_text("Entity Tracker")

def test_login_unsuccessful(setup):
    '''Tests that an unregistered user cannot log in'''
    (login_page, _) = setup
    login_page.login('b','b')
    expect(
        login_page.error_message,
        "Error message is not displayed"
    ).to_be_visible()

    expect(
        login_page.error_message,
        "Error message text is not correct"
    ).to_contain_text("Login Unsuccessful")
