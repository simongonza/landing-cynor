import re
import glob

html_files = glob.glob("*.html")
nuevo_navegacion = """          <h4 class="footer__title">Navegación</h4>
          <div class="footer__links">
            <a href="index.html" class="footer__link">Inicio</a>
            <span style="display:block; margin: 0.5rem 0 0.2rem; color: var(--text-primary); font-size: 0.9rem; font-weight: 600;">Servicios</span>
            <a href="agentes-ia.html" class="footer__link" style="font-size: 0.9rem;">— Agentes IA</a>
            <a href="automatizacion.html" class="footer__link" style="font-size: 0.9rem;">— Automatización</a>
            <a href="publicidad-digital.html" class="footer__link" style="font-size: 0.9rem;">— Publicidad</a>
            <a href="desarrollo-web.html" class="footer__link" style="font-size: 0.9rem;">— Web y Páginas</a>
            <span style="display:block; margin-top: 0.5rem;"></span>
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

print("Footer Navegación fixed in all HTML files.")
