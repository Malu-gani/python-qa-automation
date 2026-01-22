import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run_tests(playwright: Playwright):
    # Usamos chromium.launch para ver qué pasa en la pantalla
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        # --- CASO 1: HAPPY PATH ---
        print("Ejecutando Caso 1: Login Exitoso...")
        page.goto("https://the-internet.herokuapp.com/login")
        page.get_by_label("Username").fill("tomsmith")
        page.get_by_label("Password").fill("SuperSecretPassword!")
        page.get_by_role("button", name=re.compile("Login", re.IGNORECASE)).click()
        
        # Verificamos mensaje de éxito
        expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")
        print("✅ Caso 1 completado con éxito.")

        # Hacemos Logout para limpiar la sesión antes del Caso 2
        page.get_by_role("link", name="Logout").click()

        # --- CASO 2: VALID USER / INVALID PASS ---
        print("\nEjecutando Caso 2: Password Incorrecto...")
        page.goto("https://the-internet.herokuapp.com/login")
        page.get_by_label("Username").fill("tomsmith")
        page.get_by_label("Password").fill("ClaveFalsa123")
        page.get_by_role("button", name=re.compile("Login", re.IGNORECASE)).click()
        
        # Verificamos mensaje de error (cartel rojo)
        expect(page.locator("#flash")).to_contain_text("Your password is invalid!")
        print("✅ Caso 2 completado con éxito (Error detectado correctamente).")

        # --- CASO 3: INVALID USER / VALID PASS ---
        print("\nEjecutando Caso 3: Usuario incorrecto y Contraseña correcta...")
        page.goto("https://the-internet.herokuapp.com/login")
        page.get_by_label("Username").fill("el_pepe_qa")
        page.get_by_label("Password").fill("SuperSecretPassword!")
        page.get_by_role("button", name=re.compile("Login", re.IGNORECASE)).click()
        
        # Verificamos mensaje de error (cartel rojo)
        expect(page.locator("#flash")).to_contain_text("Your username is invalid!")
        print("✅ Caso 3 completado con éxito.")

        # --- CASO 4: INVALID USER / INVALID PASS ---
        print("\nEjecutando Caso 4: Ambos datos incorrectos...")
        page.goto("https://the-internet.herokuapp.com/login")
        page.get_by_label("Username").fill("el_pepe_qa")
        page.get_by_label("Password").fill("Clavefalsa123!")
        page.get_by_role("button", name=re.compile("Login", re.IGNORECASE)).click()
        
        expect(page.locator("#flash")).to_contain_text("Your username is invalid!")
        print("✅ Caso 4 completado con éxito.")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
    
    finally:
        context.close()
        browser.close()

with sync_playwright() as playwright:
    run_tests(playwright)