import pytest
import os
from datetime import datetime

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    # Solo actuamos si el test falla durante la ejecución ("call")
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            # 1. Crear carpeta si no existe
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            
            # 2. Nombre único: test_nombre_20260125.png
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"screenshots/{item.name}_{timestamp}.png"
            
            # 3. Guardar el archivo real en el disco
            page.screenshot(path=file_name)
            
            # 4. (Opcional) Vincularla visualmente al reporte HTML
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extras = getattr(report, "extras", [])
                # Creamos un bloque HTML para el reporte
                html = f'<div><img src="{file_name}" alt="screenshot" style="width:300px;height:200px;" ' \
                       f'onclick="window.open(this.src)" align="right"/></div>'
                extras.append(pytest_html.extras.html(html))
                report.extras = extras

# Mentor Mode:
# 'os' y 'datetime' son librerías estándar de Python para manejar archivos y fechas.
# 'item.name' nos da el nombre de la función que falló (ej. test_login_exitoso).
# Guardar con timestamp evita que una captura nueva pise a la anterior.