from playwright.sync_api import Page, expect
from assertpy import assert_that
from models.orange_login_page import OrangeLoginPage


def test_orange_login_success_detailed(page: Page):
    """OH-TC-01: Validar autenticación exitosa según pasos de Zephyr."""
    login = OrangeLoginPage(page)

    # --- PASO 1 ZEPHYR: Completar credenciales ---
    login.navigate()
    # Usamos los parámetros definidos en tu captura
    login.login("Admin", "admin123")

    # --- PASO 2 ZEPHYR: Esperar redirección y validar URL ---
    # Verificamos que el spinner aparezca/desaparezca y cambie la URL
    page.wait_for_url("**/dashboard/index")
    assert_that(page.url).contains("/dashboard/index")

    # --- PASO 3 ZEPHYR: Validar renderización de widgets y perfil ---

    # 1. Validamos que existan widgets en el dashboard
    widgets = page.locator(".orangehrm-dashboard-widget")
    expect(widgets.first).to_be_visible()

    # 2. SOLUCIÓN AL ERROR: Buscamos UN widget específico por su texto
    # Esto filtra los 18 elementos y se queda solo con el de "Time at Work"
    time_at_work_card = page.locator(".oxd-grid-item--gutters", has_text="Time at Work")

    # Verificamos que sea visible y tenga contenido
    expect(time_at_work_card).to_be_visible()
    assert_that(time_at_work_card.text_content()).contains("Time at Work")

    # 3. Validar nombre de perfil (Esto ya funcionaba, lo mantenemos)
    profile_name = page.locator(".oxd-userdropdown-name").text_content()
    assert_that(profile_name).is_not_empty()
