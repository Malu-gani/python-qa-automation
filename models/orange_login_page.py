from playwright.sync_api import Page


class OrangeLoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://opensource-demo.orangehrmlive.com/"
        # Selectores técnicos
        self.username_input = "xpath=//input[@name='username']"
        self.password_input = "xpath=//input[@name='password']"
        self.login_button = "xpath=//button[@type='submit']"
        # Elementos para validación de pasos 2 y 3 de Zephyr
        self.spinner = ".oxd-loading-spinner"
        self.dashboard_widgets = ".orangehrm-dashboard-widget"

    def navigate(self):
        self.page.goto(self.url)

    def login(self, user, pwd):
        # Paso 1 Zephyr: Completar campos
        self.page.fill(self.username_input, user)
        self.page.fill(self.password_input, pwd)
        self.page.click(self.login_button)
