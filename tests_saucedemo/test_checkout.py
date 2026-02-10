from playwright.sync_api import Page
from assertpy import assert_that
from models.sauce_login_page import SauceLoginPage


# SD-TC-04: Validar persistencia de estado y sesión tras recarga del navegador
def test_session_persistence_on_reload(page: Page):
    """
    Verifica que al recargar la página, el usuario permanezca logueado
    y el carrito mantenga los productos seleccionados.
    """
    login = SauceLoginPage(page)

    # 1. Step: Seleccionar un producto y hacer clic en "Add to cart"
    login.navigate()
    login.login("standard_user", "secret_sauce")
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()

    # Expected Result 1: El botón cambia a "Remove" y el carrito muestra "1"
    assert_that(page.locator("[data-test='remove-sauce-labs-backpack']")).is_not_none()
    assert_that(page.locator(".shopping_cart_badge").text_content()).is_equal_to("1")

    # 2. Step: Ejecutar una recarga de página (Refresh/F5)
    page.reload()

    # Expected Result 2: La URL permanece en inventory.html y no se solicita re-autenticación
    assert_that(page.url).contains("inventory.html")

    # 3. Step: Verificar la integridad de los datos en el encabezado
    # Expected Result 3: El contador del carrito mantiene el valor "1"
    badge_count = page.locator(".shopping_cart_badge").text_content()
    assert_that(badge_count).is_equal_to("1")


# SD-TC-05: Flujo de compra E2E con validación matemática
def test_compra_exitosa_con_validacion_precios(page: Page):
    """Realiza una compra completa validando la suma de Subtotal + Impuestos."""
    login = SauceLoginPage(page)

    login.navigate()
    login.login("standard_user", "secret_sauce")

    # Selección de producto y checkout
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator(".shopping_cart_link").click()
    page.locator("[data-test='checkout']").click()

    # Datos de envío
    page.locator("[data-test='firstName']").fill("Juan")
    page.locator("[data-test='lastName']").fill("QA")
    page.locator("[data-test='postalCode']").fill("7600")
    page.locator("[data-test='continue']").click()

    # Validación matemática antes de finalizar
    subtotal = float(
        page.locator(".summary_subtotal_label").text_content().split("$")[1]
    )
    tax = float(page.locator(".summary_tax_label").text_content().split("$")[1])
    total_web = float(page.locator(".summary_total_label").text_content().split("$")[1])

    assert_that(round(subtotal + tax, 2)).is_equal_to(total_web)

    page.locator("[data-test='finish']").click()
    assert_that(page.locator(".complete-header").text_content()).is_equal_to(
        "Thank you for your order!"
    )
