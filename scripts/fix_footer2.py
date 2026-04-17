import re
import glob

html_files = glob.glob("*.html")
nuevo_navegacion = """          <h4 class="footer__title">Navegación</h4>
          <div class="footer__links">
            <a href="index.html" class="footer__link">Inicio</a>
            <a href="index.html#soluciones" class="footer__link">Servicios</a>
            <a href="quienes-somos.html" class="footer__link">Quiénes Somos</a>
            <a href="blog.html" class="footer__link">Blog</a>
            <a href="contacto.html" class="footer__link">Contacto</a>
          </div>"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Capture from <h4 class="footer__title">Navegación</h4> to the closing </div> of <div class="footer__links">
    pattern = r'<h4 class="footer__title">Navegación</h4>\s*<div class="footer__links">.*?</div>'
    
    nuevo_contenido = re.sub(pattern, nuevo_navegacion, content, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)

print("Footer restored to simple Servicios nav item.")
