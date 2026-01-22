import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run_checkbox_tests(playwright: Playwright):
    # Configuración inicial del navegador
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        print("Iniciando Test de Checkboxes...")
        page.goto("https://the-internet.herokuapp.com/checkboxes")

        # --- PASO 1: Interactuar con los elementos ---
        # Marcamos el primero (estaba desmarcado)
        print("Marcando el primer checkbox...")
        page.get_by_role("checkbox").first.check()
        
        # Desmarcamos el segundo (estaba marcado por defecto)
        print("Desmarcando el segundo checkbox...")
        page.get_by_role("checkbox").nth(1).uncheck()

        # --- PASO 2: EXPECTED RESULT (Aserciones) ---
        # Verificamos que el primero ESTÉ marcado
        expect(page.get_by_role("checkbox").first).to_be_checked()
        
        # Verificamos que el segundo NO ESTÉ marcado
        expect(page.get_by_role("checkbox").nth(1)).not_to_be_checked()
        
        print("✅ Test completado: Los estados de los checkboxes son correctos.")

    except Exception as e:
        print(f"❌ Error durante el test: {e}")
    
    finally:
        # Pausa de 2 segundos para que puedas ver el resultado final antes de cerrar
        page.wait_for_timeout(2000) 
        context.close()
        browser.close()

with sync_playwright() as playwright:
    run_checkbox_tests(playwright)