import os
from playwright.sync_api import Page, expect
from assertpy import assert_that
from models.orange_login_page import OrangeLoginPage
from models.orange_pim_page import OrangePIMPage


def test_search_employee_by_id(page: Page):
    """OH-TC-02: Búsqueda de empleado por ID en módulo PIM."""
    login = OrangeLoginPage(page)
    pim = OrangePIMPage(page)

    # 1. Login y Acceso al módulo PIM (Paso 1 Zephyr)
    login.navigate()
    login.login("Admin", "admin123")
    pim.go_to_pim()

    # 2. Búsqueda por ID (Paso 2 Zephyr)
    # Test Data de tu captura: search_emp_id = "0312"
    pim.search_by_id("0312")
    page.wait_for_load_state("networkidle")  # Espera a que la tabla se actualice

    # 3. Validación de resultados (Paso 3 Zephyr)
    # Verificamos que la primera fila contenga el ID y el nombre esperado
    result_id = page.locator(".oxd-table-card .oxd-table-cell").nth(1).text_content()
    result_name = page.locator(".oxd-table-card .oxd-table-cell").nth(2).text_content()

    assert_that(result_id).is_equal_to("0312")
    assert_that(result_name).contains("A8DCo")  # expected_emp_name en tu captura


def test_add_new_employee(page: Page):
    """OH-TC-03: Validar la creación de un nuevo empleado en PIM."""
    login = OrangeLoginPage(page)
    pim = OrangePIMPage(page)

    # PASO 1: Login y navegación (Usando Test Data de tu captura)
    login.navigate()
    login.login("Admin", "admin123")
    pim.go_to_pim()
    pim.go_to_add_employee()

    # PASO 2: Completar formulario
    # Datos según tu Zephyr: QA_Senior, Tester_Automation, ID: 998877
    pim.fill_employee_details("QA_Senior", "Tester_Automation", "412222")

    # PASO 3: Verificación (Expected Result de Zephyr)
    # 1. Validamos el Toast de éxito
    expect(page.locator(".oxd-toast")).to_be_visible()

    # 2. El sistema redirige al perfil del empleado creado automáticamente
    # Esperamos que la URL contenga 'viewPersonalDetails'
    page.wait_for_url("**/viewPersonalDetails/**")
    assert_that(page.url).contains("viewPersonalDetails")

    # 3. Validamos que el nombre en el encabezado del perfil sea el correcto
    header_locator = page.locator(".orangehrm-edit-employee-name")
    expect(header_locator).to_contain_text("QA_Senior Tester_Automation")


def test_upload_employee_attachment(page: Page):
    """OH-TC-05: Validar la carga de archivos adjuntos en el perfil del empleado."""
    login = OrangeLoginPage(page)
    pim = OrangePIMPage(page)

    # 1. Login y navegación al perfil del empleado creado (ID: 442255)
    login.navigate()
    login.login("Admin", "admin123")
    pim.go_to_pim()
    pim.search_by_id("412222")

    # Hacemos click en el registro que aparece en la tabla para entrar al perfil
    page.locator(".oxd-table-card").first.click()

    # 2. Paso Zephyr: Subir el PDF
    # Definimos la carpeta y el nombre del archivo
    file_path = os.path.join(
        "data", "contrato-qa.pdf"
    )  # Esto arma "data/contrato-qa.pdf"

    # Obtenemos la ruta absoluta para que Playwright no se pierda
    absolute_path = os.path.abspath(file_path)

    # Verificamos si el archivo realmente existe antes de intentar subirlo (Buena práctica de QA)
    if not os.path.exists(absolute_path):
        raise FileNotFoundError(f"No se encontró el archivo en: {absolute_path}")

    # Llamamos al método del modelo
    pim.add_attachment(absolute_path, "Subida de contrato de trabajo - QA Automation")

    # 3. Verificación (Expected Result de Zephyr)
    # Validamos el mensaje de éxito
    expect(page.locator(".oxd-toast")).to_be_visible()
    expect(page.locator(".oxd-toast")).to_contain_text("Successfully Saved")

    # Validamos que el nombre del archivo aparezca en la lista de adjuntos
    # Usamos una aserción de Playwright para esperar a que aparezca en la tabla
    expect(page.locator(".orangehrm-attachment")).to_contain_text("contrato-qa.pdf")
