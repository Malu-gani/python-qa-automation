from playwright.sync_api import Page


class SauceLoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://www.saucedemo.com/"
        self.username_input = "[data-test='username']"
        self.password_input = "[data-test='password']"
        self.login_button = "[data-test='login-button']"
        self.error_container = "[data-test='error']"

    def navigate(self):
        self.page.goto(self.url)

    def login(self, user, pwd):
        self.page.fill(self.username_input, user)
        self.page.fill(self.password_input, pwd)
        self.page.click(self.login_button)

    def get_error_message(self):
        return self.page.locator(self.error_container).text_content()
