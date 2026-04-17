import re
import shutil

# Template file
base_file = "quienes-somos.html"

pages = {
    'agentes-ia.html': {
        'title': 'Agentes de Inteligencia Artificial para Empresas | Cynor',
        'desc': 'Servicios de agentes de inteligencia artificial para ventas, soporte y automatización de conversaciones en Colombia. Optimiza la atención al cliente 24/7.',
        'seo_title': 'Agentes de Inteligencia Artificial para Empresas | Cynor',
        'seo_desc': 'Automatiza la atención a clientes, perfila leads y aumenta tus ventas con agentes de inteligencia artificial 24/7.',
        'tag': 'Servicio Cynor',
        'h1': 'Agentes de <span class="text-gradient">Inteligencia Artificial</span>',
        'hero_p': 'Tus propios defensores de marca operando de forma autónoma. Un agente de inteligencia artificial atiende, califica y convierte prospectos 24 horas al día, 7 días a la semana, superando drásticamente los límites humanos en la atención y ventas.',
        'mission_tag': 'Qué son y cómo funcionan',
        'mission_h2': 'Atención inmediata,<span class="text-gradient"> conversiones incrementadas</span>',
        'mission_p1': 'Un Agente de IA no es un chatbot tradicional de menú de botones. Es una infraestructura basada en modelos de lenguaje avanzados capaz de comprender intención, contexto y manejar objeciones de ventas como un humano altamente entrenado.',
        'mission_p2': 'Al integrarlos en plataformas como WhatsApp, Instagram o tu sitio web, estos agentes perfilan a los usuarios, recuperan carritos abandonados, responden dudas de soporte técnico al instante y agendan citas automáticamente, convirtiendo el tráfico en ingresos predecibles.',
        'valores_tag': 'Casos de Uso Empresarial',
        'valores_h2': 'Aplicaciones de <span class="text-gradient">Sistemas de IA</span>',
        'val1_t': 'Fuerza de Ventas 24/7', 'val1_p': 'Atención autónoma Inbound. Nuestros agentes pueden persuadir, ofrecer productos adicionales y procesar una venta a cualquier hora.',
        'val2_t': 'Soporte al Cliente Nivel 1', 'val2_p': 'Resolución instantánea del 80% de las consultas corporativas, derivando únicamente los casos extremadamente técnicos a tus operarios.',
        'val3_t': 'Calificación de Prospectos', 'val3_p': 'Sistemas que evalúan los leads entrantes. Entrevistan al prospecto, filtran por presupuesto e intención y envían los calificados a tu CRM.',
        'val4_t': 'Agendamiento Automático', 'val4_p': 'Configura tu calendario y los agentes interactuarán con los prospectos para agendar reuniones, sincronizando todo en tu agenda principal.',
        'val5_t': 'Seguimiento Infalible', 'val5_p': 'El agente realizará follow-up automático vía WhatsApp o correo si el usuario no concreta o abandona la interacción en primer contacto.',
        'val6_t': 'Base de Conocimiento Propia', 'val6_p': 'Entrenamos a los agentes estrictamente con la información de tu empresa, asegurando que nunca inventen datos (alucinaciones controladas).',
        'res_1_t': 'Respuestas Inmediatas', 'res_1_p': 'Reducimos a cero el tiempo de espera del cliente, factor decisivo en la conversión final.',
        'res_2_t': 'Interacciones Ilimitadas', 'res_2_p': 'El agente puede sostener de 10 a 10,000 conversaciones simultáneas sin degradar la calidad.',
        'res_3_t': 'Reducción de Costos', 'res_3_p': 'Evitamos sobrecargar la contratación y disminuimos el costo promedio por atención.',
        'res_4_t': 'Unificación de Tráfico', 'res_4_p': 'Convertimos leads de meta ads más eficientemente contactándolos a WhatsApp en los primeros 5 minutos de interés.',
        'res_5_t': 'Control Total y Data', 'res_5_p': 'Todo queda registrado, y se pueden auditar conversaciones y métricas constantemente.'
    },
    'automatizacion.html': {
        'title': 'Automatización de Procesos Empresariales | Cynor',
        'desc': 'Automatización de operaciones corporativas, integración con CRM, WhatsApp y bases de datos. Escalabilidad sin crecimiento de nómina.',
        'seo_title': 'Automatización de Procesos Empresariales | Cynor',
        'seo_desc': 'Automatiza flujos de trabajo en tu empresa. Conectamos herramientas para reducir costos y trabajo manual.',
        'tag': 'Servicio Cynor',
        'h1': 'Automatización de <span class="text-gradient">Procesos Empresariales</span>',
        'hero_p': 'El trabajo repetitivo no debería depender del esfuerzo humano. Diseñamos e implementamos flujos de automatización que conectan todo el software de tu empresa, eliminando tareas manuales y reduciendo errores operativos.',
        'mission_tag': 'Integración y Funcionalidad',
        'mission_h2': 'Sistemas eficientes y <span class="text-gradient">conexiones invisibles</span>',
        'mission_p1': 'Automatizar significa que la información fluya sin que nadie la empuje. Conectamos tus formularios de captación, CRM, correo remoto, WhatsApp y bases de datos financieras en un solo sistema armonizado.',
        'mission_p2': 'Esto te permite delegar al software tares críticas como envío de facturas, nutrición de correos o asignación de prospectos al equipo comercial, logrando una operación que no duerme y reduce fricción al mínimo.',
        'valores_tag': 'Áreas de Optimización',
        'valores_h2': 'Qué puedes <span class="text-gradient">Automatizar</span>',
        'val1_t': 'Onboarding de Clientes', 'val1_p': 'Manda contratos, videos de introducción y formularios automáticamente en cuanto un pago sea procesado.',
        'val2_t': 'Integración de CRMs', 'val2_p': 'Conecta Facebook Ads, Google Ads o formularios directamente a tu CRM (Hubspot, Pipedrive) en milisegundos.',
        'val3_t': 'Recordatorios y Cobranza', 'val3_p': 'Sistemas de pagos con correos de recuperación y cobros que se envían solos a deudores y a clientes.',
        'val4_t': 'Cualificación Inbound', 'val4_p': 'Recepción de prospectos y derivación inteligente y automática según reglas empresariales.',
        'val5_t': 'Gestión de Documentos', 'val5_p': 'Genera y envía PDFs, hojas de cálculo o certificados al instante basadas en respuestas de formularios.',
        'val6_t': 'Nutrición de Leads', 'val6_p': 'Campañas automáticas de email asociadas al comportamiento del usuario con triggers avanzados.',
        'res_1_t': 'Ahorro de Tiempo Extremo', 'res_1_p': 'Libera decenas de horas semanales permitiendo a tu equipo enfocarse en cerrar tratos y no en copiar y pegar.',
        'res_2_t': 'Cero Errores Humanos', 'res_2_p': 'La tecnología no se cansa ni pierde registros. Datos exactos en el lugar correcto, de manera constante.',
        'res_3_t': 'Operación en Tiempo Real', 'res_3_p': 'Responde leads al instante de su registro para maximizar la conversión.',
        'res_4_t': 'Infraestructura Ligera', 'res_4_p': 'Evita saltar de una app a otra. Controla los procesos desde tu dashboard consolidado.',
        'res_5_t': 'Bajo Costo Marginal', 'res_5_p': 'Escalar de mil procesos automáticos a un millón cuesta casi lo mismo. Aumentas límite sin aumentar la nómina.'
    },
    'publicidad-digital.html': {
        'title': 'Publicidad Digital orientada a Performance y Conversión | Cynor',
        'desc': 'Campañas en Meta Ads y Google Ads diseñadas para conseguir leads cualificados y optimizar el retorno de inversión (ROAS).',
        'seo_title': 'Publicidad Digital orientada a Performance y Conversión | Cynor',
        'seo_desc': 'Generación de clientes potenciales con algoritmos predictivos en Meta Ads y Google Ads para negocios.',
        'tag': 'Servicio Cynor',
        'h1': 'Publicidad Digital en <span class="text-gradient">Medios de Conversión</span>',
        'hero_p': 'Dejamos atrás los likes y la exposición superficial para centrarnos en lo único que importa: ventas y clientes calificados (leads). Creamos maquinarias de captación utilizando los algoritmos de Meta Ads y Google Ads bajo lógicas de performance.',
        'mission_tag': 'Estrategia de Captación',
        'mission_h2': 'No compramos clics, <span class="text-gradient">compramos clientes</span>',
        'mission_p1': 'Mientras el mercado se enfoca en métricas de vanidad, nosotros nos enfocamos en el Costo de Adquisición (CPA) y Retorno de Inversión (ROAS). Diseñamos infraestructura que segmenta, atrae y persuade prospectos de alta intención de compra.',
        'mission_p2': 'Ya sea conectando campañas a landing pages persuasivas de alta conversión o a agentes y flujos de automatización para generar citas, logramos rastrear todo el funnel y garantizar rendimientos sólidos.',
        'valores_tag': 'Plataformas de Dominio',
        'valores_h2': 'El ecosistema <span class="text-gradient">de Tráfico</span>',
        'val1_t': 'Meta Ads (Facebook/Insta)', 'val1_p': 'Expertos en estructuración de subastas automatizadas, creativos persuasivos y audiencias Lookalike masivas.',
        'val2_t': 'Google Ads (Search)', 'val2_p': 'Interceptamos a tus clientes exactos en el momento en el que están buscando tu producto o servicio para comprar.',
        'val3_t': 'Embudos de Adquisición', 'val3_p': 'Diseñamos retargeting sofisticado, abarcando abandono de carrito o rebote con campañas dedicadas.',
        'val4_t': 'Análisis de Atribución', 'val4_p': 'Integramos la API de conversiones de manera robusta. Entendemos qué anuncio genera qué dólar de retorno.',
        'val5_t': 'Pruebas A/B Constantes', 'val5_p': 'Validamos qué creatividades (Ads) y qué ángulos de venta garantizan los costos y rentabilidad más bajos repetidamente.',
        'val6_t': 'Alineación Comercial', 'val6_p': 'Alineamos los esfuerzos de ads a tu equipo comercial, proveyendo bases de datos y leads en caliente pre-calificados.',
        'res_1_t': 'Mayor Volumen de Ventas', 'res_1_p': 'Adquirimos mayor tráfico altamente perfilado que alimenta toda tu operación in-house.',
        'res_2_t': 'Reducción de Costo de Lead', 'res_2_p': 'Disminución sistemática del CPC y CPA aplicando heurísticas y optimización estadística diaria.',
        'res_3_t': 'Segmentación Láser', 'res_3_p': 'Tus anuncios son mostrados exactamente al público con capacidad de pago e interés claro.',
        'res_4_t': 'Visibilidad Constante', 'res_4_p': 'El usuario recordará persistentemente tu marca mientras avance intencionalmente por el funnel digital.',
        'res_5_t': 'Medición Total', 'res_5_p': 'Adiós al marketing ciego. Entenderás en un dashboard cada métrica y centavo para iterar fácilmente.'
    },
    'desarrollo-web.html': {
        'title': 'Desarrollo Web de Alta Conversión y Landing Pages | Cynor',
        'desc': 'Desarrollamos ecosistemas digitales y landing pages pensadas en persuasión, métricas, y SEO técnico avanzado.',
        'seo_title': 'Desarrollo Web de Alta Conversión y Landing Pages | Cynor',
        'seo_desc': 'Desarrollo moderno, optimizado para escalar tus ventas, maximizar el SEO y acelerar el crecimiento empresarial.',
        'tag': 'Servicio Cynor',
        'h1': 'Desarrollo Web <span class="text-gradient">Orientado a Conversión</span>',
        'hero_p': 'Tu página web no puede ser solo una "tarjeta de presentación bonita". Debería ser tu principal activo de ventas, diseñada milimétricamente para convertir tráfico anónimo en clientes que deciden confiar su dinero en ti.',
        'mission_tag': 'Nuestro Enfoque',
        'mission_h2': 'Interfaces hechas <span class="text-gradient">para Vender</span>',
        'mission_p1': 'Estructuramos Landing Pages comerciales basándonos en neuroventas, fricción mínima y performance tecnológico óptimo. Desde la jerarquía visual a la velocidad de carga ultra rápida orientada a SEO y Ads.',
        'mission_p2': 'Construimos estos activos integrados inherentemente con tus bases de datos, con sistemas de agentes de inteligencia artificial y tu analítica, para asegurar que cada clic pueda ser rastreado y retenido.',
        'valores_tag': 'Arquitectura de Conversión',
        'valores_h2': 'Características <span class="text-gradient">de tu Sitio Web</span>',
        'val1_t': 'Copy Científico', 'val1_p': 'Las palabras venden. Estructuramos bloques de texto legibles, ganchos emocionales contundentes y ofertas muy claras.',
        'val2_t': 'Performance Inquebrantable', 'val2_p': 'Codificamos con tecnologías modernas enfocadas en pesos ligeros y velocidades de métricas LCP perfectas.',
        'val3_t': 'Diseño Responsive Premium', 'val3_p': 'No basta con que se adapte al móvil, está pensado prioritariamente (Mobile First) para pantallas pequeñas y touch.',
        'val4_t': 'Optimización SEO Técnica', 'val4_p': 'Estructuras on-page, datos estructurados, metadata, sitemaps y renderizado óptimo para dominar el search engine.',
        'val5_t': 'Seguridad Robusta', 'val5_p': 'Certificados modernos (SSL), arquitecturas sin vulnerabilidades y sistemas modulares altamente protegidos.',
        'val6_t': 'Conectividad a tu Stack', 'val6_p': 'Formularios y botones hiperconectados en tiempo real con Webhooks de automatización hacia tu infraestructura.',
        'res_1_t': 'Tasa de Cierre Multiplicada', 'res_1_p': 'Incremento de la tasa de visitas a lead (Conversion Rate) simplemente mitigando fricción al usuario.',
        'res_2_t': 'Posicionamiento en Google', 'res_2_p': 'Escalada en los principales buscadores lo cual provee tráfico orgánico sostenible y gratuito a lo largo del tiempo.',
        'res_3_t': 'Prestigio de la Marca', 'res_3_p': 'Un activo digital moderno transmite un nivel corporativo extremadamente alto de inmediato.',
        'res_4_t': 'Alojamiento Resiliente', 'res_4_p': 'La página responderá incluso ante altos picos de tráfico causados por publicidad viral.',
        'res_5_t': 'Tracking y Análisis', 'res_5_p': 'Etiquetado con Tag Manager y Pixel para re-alimentar tu Inteligencia Artificial publicitaria de forma perfecta.'
    }
}

with open(base_file, 'r', encoding='utf-8') as f:
    template = f.read()

for pagename, data in pages.items():
    content = template
    
    # Title & Meta
    content = re.sub(r'<title>.*?</title>', f'<title>{data["title"]}</title>', content)
    content = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{data["desc"]}">', content)
    content = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{data["seo_title"]}">', content)
    content = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{data["seo_desc"]}">', content)
    content = re.sub(r'<meta name="twitter:title" content=".*?">', f'<meta name="twitter:title" content="{data["seo_title"]}">', content)
    content = re.sub(r'<meta name="twitter:description" content=".*?">', f'<meta name="twitter:description" content="{data["seo_desc"]}">', content)
    content = re.sub(r'href="https://www.cynor.digital/quienes-somos.html"', f'href="https://www.cynor.digital/{pagename}"', content)
    content = re.sub(r'content="https://www.cynor.digital/quienes-somos.html"', f'content="https://www.cynor.digital/{pagename}"', content)
    
    # Page Hero
    content = re.sub(r'<span class="page-hero__tag reveal">.*?</span>', f'<span class="page-hero__tag reveal">{data["tag"]}</span>', content)
    content = re.sub(r'<h1 class="page-hero__title reveal delay-1">.*?</h1>', f'<h1 class="page-hero__title reveal delay-1">\n        {data["h1"]}\n      </h1>', content, flags=re.DOTALL)
    content = re.sub(r'<p class="page-hero__text reveal delay-2">.*?</p>', f'<p class="page-hero__text reveal delay-2">\n        {data["hero_p"]}\n      </p>', content, flags=re.DOTALL)
    
    # Mission Section
    content = re.sub(r'<span class="section-header__tag"\s*style="display: block; margin-bottom: var\(--space-md\); text-align: left;">.*?</span>', f'<span class="section-header__tag"\n            style="display: block; margin-bottom: var(--space-md); text-align: left;">{data["mission_tag"]}</span>', content)
    content = re.sub(r'<h2 style="margin-bottom: var\(--space-xl\);">.*?</h2>', f'<h2 style="margin-bottom: var(--space-xl);">{data["mission_h2"]}</h2>', content, flags=re.DOTALL)
    
    # We have two paragraphs in mission
    mission_p_pattern = r'<div class="reveal-left">.*?</p>.*?<p>(.*?)</p>.*?</p>.*?</div>'
    res = re.search(r'(<h2.*?>.*?</h2>\s*)<p .*?>(.*?)</p>(\s*)<p>(.*?)</p>', content, flags=re.DOTALL)
    if res:
        content = content[:res.start()] + res.group(1) + \
                  '<p style="margin-bottom: var(--space-lg);">\n            ' + data["mission_p1"] + '\n          </p>' + res.group(3) + \
                  '<p>\n            ' + data["mission_p2"] + '\n          </p>' + content[res.end():]
    
    # Valores Section
    content = re.sub(r'<span class="section-header__tag">Lo que nos define</span>', f'<span class="section-header__tag">{data["valores_tag"]}</span>', content)
    content = re.sub(r'<h2 class="section-header__title">Nuestros <span class="text-gradient">Valores</span></h2>', f'<h2 class="section-header__title">{data["valores_h2"]}</h2>', content)
    
    # Sustituir cada valor - It's easier to match all card titles and texts
    card_title_pattern = r'<h3 class="card__title text-center">(.*?)</h3>'
    card_text_pattern = r'<p class="card__text text-center">(.*?)</p>'
    
    titles = [data['val1_t'], data['val2_t'], data['val3_t'], data['val4_t'], data['val5_t'], data['val6_t']]
    texts = [data['val1_p'], data['val2_p'], data['val3_p'], data['val4_p'], data['val5_p'], data['val6_p']]
    
    def repl_title(m, i=[0]):
        try:
            val = titles[i[0]]
            i[0] += 1
            return f'<h3 class="card__title text-center">{val}</h3>'
        except IndexError:
            return m.group(0)
    def repl_text(m, i=[0]):
        try:
            val = texts[i[0]]
            i[0] += 1
            return f'<p class="card__text text-center">{val}</p>'
        except IndexError:
            return m.group(0)
            
    content = re.sub(card_title_pattern, repl_title, content)
    content = re.sub(card_text_pattern, repl_text, content)
    
    # Enfoque Section
    r_titles = [data['res_1_t'], data['res_2_t'], data['res_3_t'], data['res_4_t'], data['res_5_t']]
    r_texts = [data['res_1_p'], data['res_2_p'], data['res_3_p'], data['res_4_p'], data['res_5_p']]
    
    feature_text_pattern = r'<p class="feature-item__text"><strong>(.*?)</strong>(.*?)</p>'
    def repl_feature(m, i=[0]):
        try:
            val_t = r_titles[i[0]]
            val_p = r_texts[i[0]]
            i[0] += 1
            return f'<p class="feature-item__text"><strong>{val_t}:</strong> {val_p}</p>'
        except IndexError:
            return m.group(0)
            
    content = re.sub(feature_text_pattern, repl_feature, content)
    
    # Active Link Fix in Navbar (Change Quiénes Somos to not active)
    content = content.replace('href="quienes-somos.html" class="navbar__link active"', 'href="quienes-somos.html" class="navbar__link"')
    content = content.replace(f'href="{pagename}">', f'href="{pagename}" class="active">')
    
    with open(pagename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Pages regenerated directly from target content rules.")
