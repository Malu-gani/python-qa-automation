from playwright.sync_api import Page


class OrangePIMPage:
    def __init__(self, page: Page):
        self.page = page
        # --- Navegación y Búsqueda ---
        self.pim_menu = "xpath=//span[text()='PIM']"
        self.add_employee_btn = "xpath=//a[text()='Add Employee']"
        self.search_id_input = "xpath=//label[text()='Employee Id']/parent::div/following-sibling::div/input"
        self.search_btn = "xpath=//button[@type='submit']"

        # --- Formulario Alta ---
        self.first_name_input = "[name='firstName']"
        self.last_name_input = "[name='lastName']"
        self.employee_id_input = "xpath=//label[text()='Employee Id']/parent::div/following-sibling::div/input"
        self.save_btn = "xpath=//button[@type='submit']"

        # --- Adjuntos (OH-TC-05) ---
        self.add_attachment_btn = (
            "xpath=//h6[text()='Attachments']/following-sibling::button[text()=' Add ']"
        )
        self.file_input = "input[type='file']"
        self.file_comment = "textarea[placeholder='Type comment here']"

    def go_to_pim(self):
        self.page.click(self.pim_menu)

    def go_to_add_employee(self):
        self.page.click(self.add_employee_btn)

    def search_by_id(self, emp_id):
        self.page.fill(self.search_id_input, emp_id)
        self.page.click(self.search_btn)

    def fill_employee_details(self, first, last, emp_id):
        self.page.fill(self.first_name_input, first)
        self.page.fill(self.last_name_input, last)
        self.page.locator(self.employee_id_input).clear()
        self.page.fill(self.employee_id_input, emp_id)
        self.page.click(self.save_btn)

    def add_attachment(self, file_path, comment):
        self.page.locator(self.add_attachment_btn).scroll_into_view_if_needed()
        self.page.click(self.add_attachment_btn)
        self.page.set_input_files(self.file_input, file_path)
        self.page.fill(self.file_comment, comment)
        self.page.locator(".orangehrm-attachment").get_by_role(
            "button", name="Save"
        ).click()
