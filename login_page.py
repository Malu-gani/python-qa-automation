import re

class LoginPage:
    def __init__(self, page):
        # Guardamos la página para usarla en los métodos
        self.page = page
        
        # DEFINICIÓN DE SELECTORES: Si algo cambia en la web, solo tocás ACÁ.
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name=re.compile("Login", re.IGNORECASE))
        self.flash_message = page.locator("#flash")
        self.logout_link = page.get_by_role("link", name="Logout")

    # ACCIONES: Métodos que representan lo que un usuario hace
    def navigate(self):
        self.page.goto("https://the-internet.herokuapp.com/login")

    def submit_login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def logout(self):
        self.logout_link.click()