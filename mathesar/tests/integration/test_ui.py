import re
from playwright.sync_api import expect, Locator
from mathesar.tests.integration.utils.locators import get_table_entry


def create_new_empty_table(page):
    page.click("[aria-label='New Table']")
    page.click("button:has-text('Empty Table')")


def get_tab(page, tab_text):
    return page.locator(
        f".tab-container [role=tablist] [role=presentation]:has-text('{tab_text}')"
    )


def close_tab(tab_locator: Locator):
    tab_locator.hover()
    tab_locator.locator("[aria-label=remove]").click()


def test_tabs(page, base_schema_url):
    page.goto(base_schema_url)

    # Create Table 0
    create_new_empty_table(page)
    table_0_entry = get_table_entry(page, "Table 0")
    table_0_tab = get_tab(page, "Table 0")
    close_tab(table_0_tab)

    # Create Table 1
    create_new_empty_table(page)
    table_1_entry = get_table_entry(page, "Table 1")
    table_1_tab = get_tab(page, "Table 1")
    close_tab(table_1_tab)

    # No tabs should be open
    expect(table_0_tab).not_to_be_visible()
    expect(table_1_tab).not_to_be_visible()

    # Open Table 0
    table_0_entry.click()
    expect(table_0_entry.locator(".item")).to_have_class(re.compile("active"))
    expect(table_0_tab).to_have_class(re.compile("active"))

    # Open Table 1
    table_1_entry.click()
    expect(table_0_entry.locator(".item")).not_to_have_class(re.compile("active"))
    expect(table_1_entry.locator(".item")).to_have_class(re.compile("active"))
    expect(table_0_tab).not_to_have_class(re.compile("active"))
    expect(table_1_tab).to_have_class(re.compile("active"))

    # Switch to tab for Table 0
    table_0_tab.click()
    expect(table_0_entry.locator(".item")).to_have_class(re.compile("active"))
    expect(table_1_entry.locator(".item")).not_to_have_class(re.compile("active"))
    expect(table_0_tab).to_have_class(re.compile("active"))
    expect(table_1_tab).not_to_have_class(re.compile("active"))

    # Close tab for Table 0
    close_tab(table_0_tab)
    expect(table_0_entry.locator(".item")).not_to_have_class(re.compile("active"))
    expect(table_1_entry.locator(".item")).to_have_class(re.compile("active"))
    expect(table_0_tab).not_to_be_visible()
    expect(table_1_tab).to_have_class(re.compile("active"))

    # Close tab for Table 1
    close_tab(table_1_tab)
    expect(table_0_entry.locator(".item")).not_to_have_class(re.compile("active"))
    expect(table_1_entry.locator(".item")).not_to_have_class(re.compile("active"))
    expect(table_0_tab).not_to_be_visible()
    expect(table_1_tab).not_to_be_visible()
