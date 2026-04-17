import re
import glob

# 1. Add Blog links back to all HTML files
html_files = glob.glob("*.html")
for file in html_files:
    if file.startswith("blog"): 
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Insert in navbar
    content = re.sub(r'(<a href="quienes-somos\.html" class="navbar__link"(?: active)?>Quiénes Somos</a>)',
                     r'\1\n        <a href="blog.html" class="navbar__link">Blog</a>', content)
    # Insert in mobile menu
    content = re.sub(r'(<a href="quienes-somos\.html">Quiénes Somos</a>)',
                     r'\1\n    <a href="blog.html">Blog</a>', content)
    # Insert in footer
    content = re.sub(r'(<a href="quienes-somos\.html" class="footer__link">Quiénes Somos</a>)',
                     r'\1\n            <a href="blog.html" class="footer__link">Blog</a>', content)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Extract base template from quienes-somos.html to build the blog pages
with open('quienes-somos.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Replace active classes initially
template = template.replace('href="quienes-somos.html" class="navbar__link active"', 'href="quienes-somos.html" class="navbar__link"')

def generate_page(filename, title, description, h1, body_html):
    page = template
    page = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', page)
    page = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{description}">', page)
    
    # We will replace everything between <!-- Page Hero --> and <!-- CTA Section -->
    main_content = f'''  <!-- Page Hero -->
  <section class="page-hero" style="padding-bottom: 2rem;">
    <div class="glow-orb glow-orb--violet" style="width: 500px; height: 500px; top: -20%; right: -10%;"></div>
    <div class="container">
      <span class="page-hero__tag reveal">Blog Cynor</span>
      <h1 class="page-hero__title reveal delay-1" style="font-size: 3rem; margin-top:1rem;">
        {h1}
      </h1>
    </div>
  </section>

  <section class="section" style="padding-top: 0;">
    <div class="container" style="max-width: 800px; margin: 0 auto; color: var(--text-secondary); line-height: 1.8; font-size: 1.1rem;">
      {body_html}
    </div>
  </section>
'''
    page = re.sub(r'<!-- Page Hero -->\s*<section class="page-hero">.*?(?=<!-- CTA Section -->)', main_content, page, flags=re.DOTALL)
    
    # Mark Blog as active in navbar
    page = page.replace('<a href="blog.html" class="navbar__link">Blog</a>', '<a href="blog.html" class="navbar__link active">Blog</a>')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page)


# 3. Text for the articles
article1_body = '''
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
'''

article2_body = '''
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
'''

article3_body = '''
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
'''

generate_page('blog-automatizacion.html', 'Automatización Empresarial: Cómo Reducir Costos | Blog Cynor', 'La automatización empresarial permite a tu negocio escalar sin aumentar los gastos fijos. Descubre cómo integrar sistemas y flujos digitales de trabajo.', 'Automatización <span class="text-gradient">Empresarial</span>: Reducción de Costos', article1_body)
generate_page('blog-agentes-ia.html', 'Agentes de Inteligencia Artificial: Transformar Ventas | Blog Cynor', 'Un agente de inteligencia artificial es más que un chatbot. Descubre cómo las empresas usan IA conversacional para cualificar leads y agendar reuniones 24/7.', 'Agentes de <span class="text-gradient">Inteligencia Artificial</span> en Soporte y Ventas', article2_body)
generate_page('blog-desarrollo-web.html', 'Desarrollo Web Orientado a Conversión vs Diseño | Blog Cynor', 'Descubre por qué tu página corporativa debe apostar por la heurística comercial, usabilidad y performance antes que ser solo diseño y folleto interactivo.', 'Desarrollo Web de <span class="text-gradient">Conversión vs Solo Diseño</span>', article3_body)


# 4. Generate the blog.html Home file
blog_list_body = '''
      <div class="grid-3" style="margin-top: 3rem;">
        <div class="card card--animated reveal delay-1" style="display: flex; flex-direction: column;">
          <h3 class="card__title" style="font-size: 1.3rem; margin-bottom: 1rem;">Automatización Empresarial: Reducción de Costos</h3>
          <p class="card__text" style="flex-grow: 1; margin-bottom: 1.5rem;">La automatización empresarial interviene en los cuellos de botella del crecimiento, permitiendo que el software asuma tareas repetitivas y escalando tu operación...</p>
          <button class="btn btn--secondary" style="width: 100%; border: 1px solid rgba(255,255,255,0.1);" onclick="window.location.href='blog-automatizacion.html'">Leer artículo</button>
        </div>

        <div class="card card--animated reveal delay-2" style="display: flex; flex-direction: column;">
          <h3 class="card__title" style="font-size: 1.3rem; margin-bottom: 1rem;">Agentes de Inteligencia Artificial en Ventas</h3>
          <p class="card__text" style="flex-grow: 1; margin-bottom: 1.5rem;">A diferencia de un bot tradicional, un Agente de IA atiende prospectos corporativos 24/7, comprende la intención y agenda citas sin intervención humana...</p>
          <button class="btn btn--secondary" style="width: 100%; border: 1px solid rgba(255,255,255,0.1);" onclick="window.location.href='blog-agentes-ia.html'">Leer artículo</button>
        </div>

        <div class="card card--animated reveal delay-3" style="display: flex; flex-direction: column;">
          <h3 class="card__title" style="font-size: 1.3rem; margin-bottom: 1rem;">Desarrollo Web Orientado a Conversión</h3>
          <p class="card__text" style="flex-grow: 1; margin-bottom: 1.5rem;">Tu sitio digital no debe ser un folleto artístico. Descubre por qué priorizar CRO y arquitectura tecnológica es vital para convertir tráfico costoso en ingresos reales...</p>
          <button class="btn btn--secondary" style="width: 100%; border: 1px solid rgba(255,255,255,0.1);" onclick="window.location.href='blog-desarrollo-web.html'">Leer artículo</button>
        </div>
      </div>
'''

generate_page('blog.html', 'Blog Oficial | Empresa de Tecnología Cynor', 'Artículos especializados en inteligencia artificial, desarrollo web, publicidad e implementación de automatizaciones para empresas.', 'Blog <span class="text-gradient">Cynor</span>', blog_list_body)

print("Blog successfully built and linked in all HTML files.")
