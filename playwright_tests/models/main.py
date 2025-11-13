'''Page Object Model for Values Tracker Main Page'''
from playwright.sync_api import Page

class MainPage:
    def __init__(self, page):
        self.page = page
        self.totals_header = page.locator('[data-testid="Totals-Header"]')
        self.totals_chart = page.locator(
            '//h1[@data-testid="Totals-Header"]/following::div[1]/*[@class="recharts-responsive-container"]'
        )
        self.tooltip_label = page.locator('[class="recharts-tooltip-label"]')
        self.tooltip_item = page.locator('[class="recharts-tooltip-item"]')

    def chart_header(self, chart_header):
        return self.page.locator(f'[data-testid="{chart_header}-Header"]')

    def entity_chart(self, chart_header):
        return self.page.locator(
            f'//h1[@data-testid="{chart_header}-Header"]/following::*[@class="recharts-responsive-container"][1]'
        )
