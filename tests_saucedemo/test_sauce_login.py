from playwright.sync_api import Page
from assertpy import assert_that
from models.sauce_login_page import SauceLoginPage


# SD-TC-01: Happy Path
def test_valid_login(page: Page):
    login = SauceLoginPage(page)
    login.navigate()
    login.login("standard_user", "secret_sauce")
    assert_that(page.url).contains("inventory.html")


# SD-TC-02: Negative Testing (Locked User)
def test_locked_out_user(page: Page):
    login = SauceLoginPage(page)
    login.navigate()
    login.login("locked_out_user", "secret_sauce")
    assert_that(login.get_error_message()).contains("locked out")


# SD-TC-03: Campos Vacíos
def test_empty_fields_error(page: Page):
    login = SauceLoginPage(page)
    login.navigate()
    login.login("", "")  # Intento de login vacío
    assert_that(login.get_error_message()).contains("Username is required")
