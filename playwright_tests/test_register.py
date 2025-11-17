'''Tests the Register page UI'''
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
        LoginPage(page).register_link.dblclick()
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
    (register_page, _) = setup
    expect(
        register_page.email_input,
        "Submit button is not displayed"
    ).to_be_visible()
    expect(
        register_page.email_input,
        "Submit button is not correct"
    ).to_contain_text("Submit")

