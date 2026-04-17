import json
import os
import re

# Ensure directory exists for json
os.makedirs('data', exist_ok=True)
os.makedirs('js', exist_ok=True)

# 1. Create posts.json
posts = [
    {
        "id": "automatizacion-empresarial",
        "titulo": "Automatización Empresarial: Reducción de Costos",
        "fecha": "17 Abril 2026",
        "categoria": "Automatización",
        "resumen": "La automatización empresarial interviene en los cuellos de botella del crecimiento, permitiendo que el software asuma tareas repetitivas y escalando tu operación...",
        "imagen": "src/blog1.png",
        "contenido": """
      <p style="margin-bottom: 1.5rem;">Las empresas tradicionales se enfrentan a menudo a un "techo de cristal" de crecimiento: cuantos más clientes obtienen, más carga operativa manual se genera. Contratar más personal parece ser la única salida, aumentando los costos fijos y reduciendo el margen de beneficio. Sin embargo, la automatización empresarial interviene exactamente en este cuello de botella, permitiendo que el software asuma tareas repetitivas y liberando a tu equipo para el trabajo verdaderamente estratégico.</p>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">¿Qué significa realmente automatizar una empresa?</h2>
      <p style="margin-bottom: 1.5rem;">No hablamos de simples atajos de teclado, sino de un ecosistema interconectado. Imagina que el llenado de un formulario en tu sitio web conecte directamente a tu CRM, genere una factura en tu software contable y envíe un correo de bienvenida automático al cliente, todo en milisegundos y sin la intervención de una mano humana.</p>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">Beneficios Cuantificables</h2>
      <ul style="margin-bottom: 1.5rem; padding-left: 1.5rem; list-style-type: disc;">
         <li style="margin-bottom: 0.8rem;"><strong style="color:var(--text-primary);">Reducción Inmediata de Errores Operativos:</strong> Un software no comete errores tipográficos ni olvida enviar correos de seguimiento. Todo ocurre con exactitud programada.</li>
         <li style="margin-bottom: 0.8rem;"><strong style="color:var(--text-primary);">Aplanamiento de la Curva de Costos:</strong> Al automatizar procesos de soporte técnico, facturación o ingreso de datos, la empresa puede escalar y absorber hasta 10 veces más volumen sin necesidad de multiplicar su personal o incurrir en horas extras.</li>
         <li style="margin-bottom: 0.8rem;"><strong style="color:var(--text-primary);">Agilidad Competitiva:</strong> El prospecto actual espera respuestas inmediatas. Mientras una empresa humana tarda 3 horas en responder a un lead, un sistema automatizado toma menos de 2 segundos.</li>
      </ul>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">Ejemplo Práctico en Consultorías B2B</h2>
      <p style="margin-bottom: 1.5rem;">Una firma financiera recibía unos 30 contactos al día. Su personal gastaba más de tres horas organizándolos en un Excel y enviando manualmente folletos en PDF. Implementamos un sistema que no solo guarda y cualifica los contactos automáticamente (CRM), sino que distribuye seguimientos espaciados por correo (Nutrición) si el cliente no responde. Resultado: ahorro de 20 horas semanales por equipo y un incremento del 200% de conversión al atender en el acto.</p>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">Conclusión</h2>
      <p style="margin-bottom: 1.5rem;">El trabajo manual repetitivo es el activo más costoso de cualquier compañía moderna. Escalar sin ordenizar y sistematizar los procesos solo acelera el caos. Integrar automatizaciones no elimina al talento humano, sino que lo reasigna a áreas donde verdaderamente aporta valor y retorno de inversión.</p>
      <p style="padding: 1.5rem; border-left: 4px solid var(--color-violet); background: rgba(138, 43, 226, 0.05); margin-top: 2rem; color:var(--text-primary);"><em>¿Tu empresa gasta demasiado tiempo en tareas manuales? Conoce cómo en Cynor conectamos e implementamos sistemas de automatización personalizados para tu operación.</em></p>
        """
    },
    {
        "id": "agentes-ia",
        "titulo": "Agentes de Inteligencia Artificial en Ventas",
        "fecha": "16 Abril 2026",
        "categoria": "Inteligencia Artificial",
        "resumen": "A diferencia de un bot tradicional, un Agente de IA atiende prospectos corporativos 24/7, comprende la intención y agenda citas sin intervención humana...",
        "imagen": "src/blog2.png",
        "contenido": """
      <p style="margin-bottom: 1.5rem;">La forma en que los consumidores y las empresas compran ha cambiado radicalmente en los últimos tres años. La inmediatez ya no es negociable, sino el estandar base. Históricamente, las empresas intentaban abordar esta necesidad añadiendo centros de atención o usando "chatbots" de respuestas rígidas (y muy frustrantes). Hoy, la llegada de los Agentes de Inteligencia Artificial basados en Grandes Modelos de Lenguaje (LLMs) marca un antes y un después en la experiencia de cierre y atención comercial.</p>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">No es un Chatbot, es un Asistente Corporativo</h2>
      <p style="margin-bottom: 1.5rem;">A diferencia de un bot tradicional con un árbol de opciones, un agente de IA puede comprender la intención real del texto, revisar el inventario en tiempo real, recordar contexto de mensajes pasados y formular respuestas naturales. Su misión no es "desviar los mensajes", sino resolver o vender proactivamente.</p>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">El Rol del Agente de IA Comercial</h2>
      <ul style="margin-bottom: 1.5rem; padding-left: 1.5rem; list-style-type: disc;">
         <li style="margin-bottom: 0.8rem;"><strong style="color:var(--text-primary);">Disponibilidad Total (24/7/365):</strong> A las 3:00 de la madrugada, un domingo festivo, si tu pauta digital capta la curiosidad de un directivo, tu agente comercial es capaz de cualificarlo, resolver objeciones e incluso agendar de inmediato en tu calendario antes de que se enfríe su impulso.</li>
         <li style="margin-bottom: 0.8rem;"><strong style="color:var(--text-primary);">Capacidad Analítica de Prospectos:</strong> Antes de derivar un contacto al equipo de ventas de cierre corporativo, el IA discriminará el tamaño de la cuenta o su intención presupuestal. Solamente filtrará hacia los ejecutivos a los "Leads Calientes".</li>
         <li style="margin-bottom: 0.8rem;"><strong style="color:var(--text-primary);">Manejo de Objeciones Escalables:</strong> Alimentado con tu propia "Base de Conocimiento", el Agente sabrá manejar dudas sobre políticas de servicio, devoluciones y tiempos de entrega mejor que cualquier empleado no capacitado.</li>
      </ul>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">Ejemplo Práctico en Seguros o Salud</h2>
      <p style="margin-bottom: 1.5rem;">Una compañía médica implementó un agente de IA en su WhatsApp Corporativo. Anteriormente, la central colapsaba agendando turnos rutinarios. Ahora, el Agente solicita número de ID, verifica agendas de doctores vacantes disponibles vía base de datos oculta, confirma el turno y envía el recordatorio 24h antes del encuentro. Las ausencias del personal caen un 50% y los recepcionistas se dedican pura y exclusivamente a coordinar atención presencial sofisticada.</p>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">Conclusión</h2>
      <p style="margin-bottom: 1.5rem;">Entregarle toda la atención primaria humana (Layer 1) a una entidad sintética no es sólo un ejercicio tecnológico futurista, es una estrategia inmediata de recortes de tiempos. Mientras tus competidores están haciendo esperar 6 horas a sus clientes de alto valor, tú estarás cerrándolos en milisegundos con fluidez comunicacional.</p>
      <p style="padding: 1.5rem; border-left: 4px solid var(--color-violet); background: rgba(138, 43, 226, 0.05); margin-top: 2rem; color:var(--text-primary);"><em>Implementa asistentes precisos para tu WhatsApp o sitio web. En Cynor construimos e integramos infraestructuras de IA sin alucinaciones, entrenadas con tus datos.</em></p>
        """
    },
    {
        "id": "desarrollo-web-conversion",
        "titulo": "Desarrollo Web Orientado a Conversión",
        "fecha": "15 Abril 2026",
        "categoria": "Desarrollo y Conversión",
        "resumen": "Tu sitio digital no debe ser un folleto artístico. Descubre por qué priorizar CRO y arquitectura tecnológica es vital para convertir tráfico costoso...",
        "imagen": "src/blog3.png",
        "contenido": """
      <p style="margin-bottom: 1.5rem;">Uno de los errores más caros que cometen las corporaciones (Startups y Pymes por igual) es encargar la elaboración de su sitio digital web a diseñadores tradicionales o estudios artísticos creativos que valoran puramente la estética por encima de la fricción comercial. El resultado inevitable es una página espectacular que asombra visualmente, pero se vuelve extremadamente incapaz de convertir ese tráfico publicitario costoso en ingresos, retornos y ventas medibles.</p>
      <p style="margin-bottom: 1.5rem;">El desarrollo web ha mutado; hoy un sitio no es algo que se "cuelga de la web" para que exista el folleto de la empresa. Se ha convertido en tu activo número uno dedicado a la fricción de ventas: una Landing Page Optimizada.</p>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">¿Qué es el Desarrollo Web Orientado a Conversión?</h2>
      <p style="margin-bottom: 1.5rem;">Consiste en ingeniería aplicada que prioriza sistemáticamente una estructura UX (User Experience) lógica que empuja al usuario sin obligarlo hacia una decisión firme: llamar, comprar, dejar sus datos o agendar un encuentro. A este enfoque se le aplica habitualmente CRO (Conversion Rate Optimization).</p>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">Diferenciadores Clave para tu Tráfico Web</h2>
      <ul style="margin-bottom: 1.5rem; padding-left: 1.5rem; list-style-type: disc;">
         <li style="margin-bottom: 0.8rem;"><strong style="color:var(--text-primary);">Velocidad de Carga por encima de las Animaciones:</strong> Según Google, cada segundo que tarda tu web en cargar eleva la tasa de rebote abruptamente. Imágenes excesivas de alta calidad gráfica destruyen un posible "lead" móvil antes de que visualicen el mensaje central. Nuestro parámetro de programación y desarrollo descabellado es apuntar debajo de algoritmos perfectos 1.0 segundos.</li>
         <li style="margin-bottom: 0.8rem;"><strong style="color:var(--text-primary);">Mapas de Calor y Tracking:</strong> Tu página no termina cuando se publica. Deben programarse y ejecutarse píxeles invisibles, API de conversiones para nutrir la pauta de Facebook/Google y scripts que demuestren qué tan adentro navega la visita (Heatmaps).</li>
         <li style="margin-bottom: 0.8rem;"><strong style="color:var(--text-primary);">Escaneabilidad Vs Creatividad:</strong> Las personas no leen las webs corporativas o landing pages, "escanean". La jerarquía en negrita, uso de checklists, fondos oscuros (baja luminosidad fatiga visual), títulos enormes resolutivos y CTAs contrastantes son las que cierran facturas directas.</li>
      </ul>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">El Ejemplo Práctico en B2B Inmobiliario</h2>
      <p style="margin-bottom: 1.5rem;">Un desarrollador de inmuebles tenía un sitio de lujo hecho 100% en video interactivo y arte, donde los inversionistas debían hacer múltiples clics artísticos para llegar a los asesores. Una vez implementamos nuestro enfoque de Conversión Optimizada, acortamos todos los tiempos quitando la intro. Colocamos una oferta explícita visible "sin tener que girar la rueda" (Above-The-Fold), y anclamos el formulario a WhatsApp Integrado. Con exactamente el presupuesto orgánico se sextuplicó el volumen de clientes perfilados contactados diariamente.</p>
      
      <h2 style="color: var(--text-primary); margin-top: 2.5rem; margin-bottom: 1rem; font-size: 1.8rem;">Conclusión</h2>
      <p style="margin-bottom: 1.5rem;">La frase "Tu inversión web se pagará sola" solamente aplica si la arquitectura digital fue montada meticulosamente para procesar extraños y arrojar dinero mensualmente. Estética más ingeniería y rendimiento dan como resultado un activo altamente rentable comercial. Lo opuesto otorga una obra de arte inútil.</p>
      <p style="padding: 1.5rem; border-left: 4px solid var(--color-violet); background: rgba(138, 43, 226, 0.05); margin-top: 2rem; color:var(--text-primary);"><em>Tu página es el motor fundamental y base de toda red publicitaria. Descubre cómo Cynor modela interfaces persuasivas con código puro conectadas directamente a tus métricas empresariales.</em></p>
        """
    }
]

with open('data/posts.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

# 2. Add js/blog.js
blog_js = """
// Blog SPA Logic
let blogPosts = [];

async function initBlog() {
    try {
        const response = await fetch('data/posts.json');
        blogPosts = await response.json();
        
        // Check hash to see if we should load a post
        handleHashChange();
        
        // Listen to hash changes for browser back/forward buttons
        window.addEventListener('hashchange', handleHashChange);
    } catch (e) {
        console.error('Error loading blog posts:', e);
    }
}

function handleHashChange() {
    const hash = window.location.hash.substring(1);
    if (hash && hash.startsWith('post-')) {
        const postId = hash.replace('post-', '');
        const post = blogPosts.find(p => p.id === postId);
        if (post) {
            renderPost(post);
            return;
        }
    }
    // Default: render list
    renderList();
}

function renderList() {
    const listContainer = document.getElementById('blog-list');
    const postContainer = document.getElementById('blog-post');
    const heroTitle = document.getElementById('blog-hero-title');
    
    // UI toggles
    listContainer.style.display = 'grid';
    postContainer.style.display = 'none';
    if(heroTitle) heroTitle.innerHTML = 'Blog <span class="text-gradient">Cynor</span>';
    
    // Clear and populate grid
    listContainer.innerHTML = '';
    
    blogPosts.forEach((post, i) => {
        const delayClass = `delay-${(i % 3) + 1}`;
        const cardHTML = `
        <div class="card card--animated reveal ${delayClass}" style="display: flex; flex-direction: column; padding: 0; overflow: hidden; cursor:pointer;" onclick="window.location.hash='post-${post.id}'">
          <img src="${post.imagen}" alt="${post.titulo}" style="width: 100%; height: 200px; object-fit: cover;">
          <div style="padding: 1.5rem; display: flex; flex-direction: column; flex-grow: 1;">
            <div style="font-size: 0.8rem; color: var(--color-violet); font-family: 'Orbitron', monospace; margin-bottom: 0.5rem;">${post.categoria} &bull; ${post.fecha}</div>
            <h3 style="font-family: 'DM Sans', sans-serif; font-size: 1.25rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1rem; line-height: 1.4;">${post.titulo}</h3>
            <p class="card__text" style="flex-grow: 1; margin-bottom: 1.5rem; font-size: 0.95rem;">${post.resumen}</p>
            <button class="btn btn--secondary" style="width: 100%; border: 1px solid rgba(255,255,255,0.1);">Leer artículo</button>
          </div>
        </div>
        `;
        listContainer.insertAdjacentHTML('beforeend', cardHTML);
    });
}

function renderPost(post) {
    const listContainer = document.getElementById('blog-list');
    const postContainer = document.getElementById('blog-post');
    const heroTitle = document.getElementById('blog-hero-title');
    
    // Build post HTML
    // A nice back button
    const html = `
        <button class="btn btn--secondary" style="margin-bottom: 2rem; padding: 10px 20px; font-size: 0.9rem;" onclick="window.location.hash=''">← Volver al Blog</button>
        <img src="${post.imagen}" style="width: 100%; height: auto; max-height: 400px; object-fit: cover; border-radius: var(--radius-lg); margin-bottom: 2rem;">
        <div style="color: var(--color-violet); font-family: 'Orbitron', monospace; margin-bottom: 1rem;">${post.categoria} &bull; ${post.fecha}</div>
        <h1 style="font-family: 'Orbitron', sans-serif; font-size: 2.5rem; margin-bottom: 2rem; line-height: 1.2;">${post.titulo}</h1>
        <div style="line-height: 1.8; font-size: 1.1rem; color: var(--text-secondary);">
            ${post.contenido}
        </div>
    `;
    
    postContainer.innerHTML = html;
    
    // UI toggles
    listContainer.style.display = 'none';
    postContainer.style.display = 'block';
    
    // Optional: Update hero
    if(heroTitle) heroTitle.innerHTML = `<span style="font-size: 1.5rem; opacity: 0.8;">Blog Cynor</span>`;
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Start
document.addEventListener('DOMContentLoaded', initBlog);
"""

with open('js/blog.js', 'w', encoding='utf-8') as f:
    f.write(blog_js)

# 3. Update blog.html specifically
with open('blog.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the grid-3 container with the SPA containers and link JS
spa_html = """
      <!-- SPA Views Container -->
      <div id="blog-list" class="grid-3" style="margin-top: 3rem;">
        <!-- Filled by JS -->
      </div>
      
      <div id="blog-post" style="display: none; margin-top: 2rem;" class="reveal">
        <!-- Filled by JS -->
      </div>
"""

# RegEx the old grid
content = re.sub(r'<div class="grid-3" style="margin-top: 3rem;">.*?</div>(?=\s*</div>\s*</section>)', spa_html, content, flags=re.DOTALL)
content = content.replace('id="blog-hero-title"', '') # Ensure clean
content = content.replace('<h1 class="page-hero__title reveal delay-1" style="font-size: 3rem; margin-top:1rem;">', '<h1 id="blog-hero-title" class="page-hero__title reveal delay-1" style="font-size: 3rem; margin-top:1rem;">')

# Ensure script is included before body close
if '<script src="js/blog.js"></script>' not in content:
    content = content.replace('<script src="js/main.js"></script>', '<script src="js/main.js"></script>\n  <script src="js/blog.js"></script>')

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(content)

# 4. Remove the old individual pages
for old_file in ['blog-automatizacion.html', 'blog-agentes-ia.html', 'blog-desarrollo-web.html']:
    try:
        os.remove(old_file)
    except OSError:
        pass

print("Blog refactored to SPA")
