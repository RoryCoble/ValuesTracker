'''Tests the ApiRequest module the UI uses to call the Api'''
import pytest
from playwright.sync_api import sync_playwright, expect
from tests.setup_functions import SetupFunctions
from .models.login import LoginPage
from .models.main import MainPage
from .models.all import AllPage

@pytest.fixture(scope='session', name='setup')
def fixture_setup():
    """Creates the expected test data, renders the browser page, 
    then cleans up any added data after the tests have run"""
    SetupFunctions().truncate_entities()
    SetupFunctions().truncate_users()

    # Create and attach user here
    with sync_playwright() as playwright:
        browser = playwright.webkit.launch()
        context = browser.new_context()
        page = context.new_page()
        all_page = AllPage(page)
        all_page.create_user('a','a','a')
        all_page.add_entity('AAAAA', 'Volatile', 7.2)
        all_page.add_entity('BBBBB', 'Volatile', 2.2)
        all_page.connect_user_entity('a','AAAAA')
        all_page.connect_user_entity('a','BBBBB')
        aaaaa_value = all_page.generate_value('1','AAAAA').json()
        bbbbb_value = all_page.generate_value('1','BBBBB').json()
        LoginPage(page).login('a','a')
        yield (MainPage(page), aaaaa_value, bbbbb_value, all_page)

    SetupFunctions().truncate_users()
    SetupFunctions().truncate_entities()

def test_page_displays(setup):
    '''Tests that the Main page displays as expected'''
    (main_page, aaaaa_value, bbbbb_value, all_page) = setup

    expect(
        all_page.page_title,
        "Page title is not displayed"
    ).to_be_visible()
    expect(
        all_page.page_title,
        "Page title text does not match"
    ).to_contain_text("Entity Tracker")

    expect(
        main_page.totals_header,
        "Totals chart header is not displayed"
    ).to_be_visible()
    expect(
        main_page.totals_header,
        "Totals chart header does not match"
    ).to_contain_text("Totals")

    expect(
        main_page.totals_chart,
        "Totals chart is not displayed"
    ).to_be_visible()
    main_page.totals_chart.hover()
    expect(
        main_page.tooltip_label.filter(has_text="1"),
        "Tooltip Label is not displayed"
    ).to_be_visible()
    expect(
        main_page.tooltip_item.filter(has_text="AAAAA"),
        "Tooltip values are not displayed"
    ).to_be_visible()
    expect(
        main_page.tooltip_item.filter(has_text="AAAAA"),
        "Tooltip value does not contain expected data"
    ).to_contain_text(f"AAAAA : {aaaaa_value}")
    expect(
        main_page.tooltip_item.filter(has_text="BBBBB"),
        "Tooltip values are not displayed"
    ).to_be_visible()
    expect(
        main_page.tooltip_item.filter(has_text="BBBBB"),
        "Tooltip value does not contain expected data"
    ).to_contain_text(f"BBBBB : {bbbbb_value}")
