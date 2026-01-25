from playwright.sync_api import Page, expect
from login_page import LoginPage
import pytest

# Mentor Mode: Al usar 'page' como argumento, Pytest-Playwright
# se encarga de abrir y cerrar el navegador automáticamente.

def test_login_exitoso(page: Page):
    login = LoginPage(page)
    login.navigate()
    login.submit_login("tommith", "SuperSecretPassword!")
    expect(login.flash_message).to_contain_text("You logged into a secure area!")

def test_login_password_incorrecto(page: Page):
    login = LoginPage(page)
    login.navigate()
    login.submit_login("tomsmith", "ClaveFalsa123")
    expect(login.flash_message).to_contain_text("Your password is invalid!")

def test_login_usuario_incorrecto(page: Page):
    login = LoginPage(page)
    login.navigate()
    login.submit_login("usuario_inexistente", "SuperSecretPassword!")
    expect(login.flash_message).to_contain_text("Your username is invalid!")
    