import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run_dropdown_test(playwright: Playwright) -> None:
    # Configuración inicial
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        print("Iniciando Test de Dropdown...")
        page.goto("https://the-internet.herokuapp.com/dropdown")

        # --- PASO 1: Seleccionar Opción 1 ---
        print("Seleccionando 'Option 1'...")
        # El valor interno en el HTML es "1"
        page.locator("#dropdown").select_option("1")
        
        # VALIDACIÓN: ¿Realmente se seleccionó el valor "1"?
        expect(page.locator("#dropdown")).to_have_value("1")
        print("✅ Opción 1 seleccionada y validada.")

        # --- PASO 2: Seleccionar Opción 2 ---
        print("Seleccionando 'Option 2'...")
        # El valor interno en el HTML es "2"
        page.locator("#dropdown").select_option("2")
        
        # VALIDACIÓN: ¿Realmente cambió al valor "2"?
        expect(page.locator("#dropdown")).to_have_value("2")
        print("✅ Opción 2 seleccionada y validada.")

    except Exception as e:
        print(f"❌ Error durante el test: {e}")

    finally:
        # Pausa para inspección visual antes de cerrar
        page.wait_for_timeout(2000)
        print("Cerrando navegador...")
        context.close()
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run_dropdown_test(playwright)