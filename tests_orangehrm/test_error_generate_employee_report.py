import os
from playwright.sync_api import Page, expect
from assertpy import assert_that
from models.orange_login_page import OrangeLoginPage
from models.orange_pim_page import OrangePIMPage


def test_generate_employee_report(page: Page):
    """OH-TC-10: Generación de reporte de empleados (Custom Report)."""
    login = OrangeLoginPage(page)
    pim = OrangePIMPage(page)
    report_name = "PIM Sample Report"

    # PASO 1: Navegación
    login.navigate()
    login.login("Admin", "admin123")
    pim.go_to_pim()
    pim.go_to_reports()

    # PASO 2: Localizar el reporte con la nueva lógica de sugerencias
    pim.search_report(report_name)

    # PASO 3: Ejecutar reporte (Run)
    # 1. Ubicamos la fila del reporte específico
    report_row = page.locator(".oxd-table-card", has_text=report_name)

    # 2. En OrangeHRM, el botón de 'Run' es el icono de la derecha (el archivo con el gráfico)
    # Usamos la clase de la "lupa" o el "archivo" que suele ser .bi-display o .bi-file-text
    # Pero lo más seguro es buscar el botón que está al final de la fila:
    run_button = report_row.locator(
        "button i.bi-file-text-fill, button i.bi-display"
    ).first

    # 3. Forzamos el click
    run_button.click()

    # PASO 4: Exportar a CSV y validar descarga
    # 1. Esperamos a que la tabla de resultados cargue (Paso 3 Zephyr)
    # Según tu captura image_0f0c42.png, ya estamos en la vista de datos
    page.wait_for_selector(".orangehrm-paper-container")

    # 2. Capturamos la descarga al hacer click en el botón CSV
    # Intentamos localizar el botón por su rol o texto, que es lo más estable
    with page.expect_download() as download_info:
        # En esta pantalla, el botón suele decir 'CSV' o tener un icono específico
        page.get_by_role("button", name="CSV").click()

    download = download_info.value

    # 3. Verificación técnica
    print(f"Archivo descargado: {download.suggested_filename}")
    assert ".csv" in download.suggested_filename.lower()

    # Guardamos el reporte en tu carpeta data
    download.save_as(os.path.join("data", download.suggested_filename))
