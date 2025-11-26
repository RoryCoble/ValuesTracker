'''Tests the Main page UI'''
import pytest
from playwright.sync_api import sync_playwright, expect
from tests.setup_functions import SetupFunctions
from .models.login import LoginPage
from .models.main import MainPage
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

def test_page_title(setup):
    '''Tests that the Main page's title'''
    (_, _, _, all_page) = setup
    all_page.test_page_title('Entity Tracker')

def test_totals_chart(setup):
    '''Tests the Totals chart'''
    (main_page, aaaaa_value, bbbbb_value, _) = setup

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

def test_aaaaa_chart(setup):
    '''Tests the AAAAA chart'''
    (main_page, aaaaa_value, _, _) = setup

    expect(
        main_page.chart_header('AAAAA'),
        "AAAAA chart header does not display"
    ).to_be_visible()
    expect(
        main_page.chart_header('AAAAA'),
        "AAAAA chart header does not read AAAAA"
    ).to_contain_text('AAAAA')
    expect(
        main_page.entity_chart('AAAAA'),
        "AAAAA chart is not displayed"
    ).to_be_visible()
    main_page.entity_chart('AAAAA').hover()
    expect(
        main_page.tooltip_label.filter(has_text="1"),
        "Tooltip Label is not displayed"
    ).to_be_visible()
    expect(
        main_page.tooltip_item.filter(has_text="value"),
        "Tooltip value does not contain expected data"
    ).to_contain_text(f"value : {aaaaa_value}")

def test_bbbbb_chart(setup):
    '''Tests the BBBBB chart'''
    (main_page, _, bbbbb_value, _) = setup

    expect(
        main_page.chart_header('BBBBB'),
        "BBBBB chart header does not display"
    ).to_be_visible()
    expect(
        main_page.chart_header('BBBBB'),
        "BBBBB chart header does not read BBBBB"
    ).to_contain_text('BBBBB')
    expect(
        main_page.entity_chart('BBBBB'),
        "BBBBB chart is not displayed"
    ).to_be_visible()
    main_page.entity_chart('BBBBB').hover()
    expect(
        main_page.tooltip_label.filter(has_text="1"),
        "Tooltip Label is not displayed"
    ).to_be_visible()
    expect(
        main_page.tooltip_item.filter(has_text="value"),
        "Tooltip value does not contain expected data"
    ).to_contain_text(f"value : {bbbbb_value}")
