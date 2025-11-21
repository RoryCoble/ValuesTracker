'''Tests the Register page UI'''
import re
import pytest
from playwright.sync_api import sync_playwright, expect
from tests.setup_functions import SetupFunctions
from .models.login import LoginPage
from .models.register import RegisterPage
from .models.all import AllPage

@pytest.fixture(scope='class', name='setup')
def fixture_setup():
    """Creates the expected test data, renders the browser page, 
    then cleans up any added data after the tests have run"""
    SetupFunctions().truncate_users()

    # Create and attach user here
    with sync_playwright() as playwright:
        page = playwright.webkit.launch().new_context().new_page()
        all_page = AllPage(page)
        page.goto('http://localhost:3000/')
        LoginPage(page).register_button.click()
        yield (RegisterPage(page), all_page)

    SetupFunctions().truncate_users()

def test_page_title(setup):
    '''Tests that the Register page's title'''
    (_, all_page) = setup
    all_page.test_page_title('Register')

def tests_username_input_displays(setup):
    '''Tests that the Username input displays'''
    (register_page, _) = setup
    expect(
        register_page.username_input,
        "Username input is not displayed"
    ).to_be_visible()
    expect(
        register_page.username_input,
        "Username placeholder is not correct"
    ).to_have_attribute("placeholder", "User Name")

def tests_password_input_displays(setup):
    '''Tests that the Password input displays'''
    (register_page, _) = setup
    expect(
        register_page.password_input,
        "Password input is not displayed"
    ).to_be_visible()
    expect(
        register_page.password_input,
        "Password placeholder is not correct"
    ).to_have_attribute("placeholder", "Password")

def tests_email_input_displays(setup):
    '''Tests that the Email input displays'''
    (register_page, _) = setup
    expect(
        register_page.email_input,
        "Password input is not displayed"
    ).to_be_visible()
    expect(
        register_page.email_input,
        "Password placeholder is not correct"
    ).to_have_attribute("placeholder", "Email")

def tests_submit_button_displays(setup):
    '''Tests that the Submit button displays'''
    (register_page, _) = setup
    expect(
        register_page.submit_button,
        "Submit button is not displayed"
    ).to_be_visible()
    expect(
        register_page.submit_button,
        "Submit button text is not correct"
    ).to_contain_text("Submit")

def tests_cancel_button_displays(setup):
    '''Tests that the Cancel link displays'''
    (register_page, _) = setup
    expect(
        register_page.cancel_button,
        "Cancel button is not displayed"
    ).to_be_visible()
    expect(
        register_page.cancel_button,
        "Cancel button text is not correct"
    ).to_contain_text("Cancel")

def tests_cancel_returns_to_login(setup):
    '''
    Tests that clicking the Cancel button returns the user
    to the Login page
    '''
    (register_page, _) = setup
    register_page.cancel_button.click()
    expect(register_page.page).to_have_url(re.compile("/login"))

def tests_user_can_register(setup):
    '''Tests that the user can register themselves'''
    (register_page, _) = setup
    register_page.register_user("a", "a", "a")
    expect(register_page.page).to_have_url(re.compile("/login"))
