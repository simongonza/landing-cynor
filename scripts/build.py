#!/usr/bin/env python3
"""Arma las páginas del sitio a partir de pages/*.html y templates/.

Cada archivo en pages/ empieza con un bloque de metadatos:

    <!--meta
    {"title": "...", "description": "...", "path": "/salud", "nav": "salud"}
    -->

y puede incluir piezas compartidas con <!-- include: nombre --> (templates/partials/nombre.html).
El resultado se escribe en la raíz del repo (salud.html, index.html, ...), que es lo que publica Cloudflare Pages.

Los artículos y vlogs del blog viven en content/blog/*.html (bloque <!--meta {...} --> con
titulo, slug, fecha AAAA-MM-DD, categoria, tipo "articulo" o "vlog", resumen, imagen y, para
vlogs, video, duracion y transcripcion). Cada uno se publica en /blog/<slug> y la lista de
/blog se arma sola; no hace falta tocar JavaScript para publicar.

Uso: python3 scripts/build.py
"""
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
TEMPLATES = ROOT / "templates"
POSTS_DIR = ROOT / "content" / "blog"
OG_DEFAULT = "https://www.cynor.digital/src/og-cynor.png"
SITE = "https://www.cynor.digital"

ORGANIZATION = {
    "@type": "Organization",
    "@id": f"{SITE}/#organization",
    "name": "Cynor",
    "url": f"{SITE}/",
    "logo": f"{SITE}/src/Logo.png",
    "slogan": "Innovation that thinks in data.",
    "address": {"@type": "PostalAddress", "addressLocality": "Medellín", "addressCountry": "CO"},
    "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+57 312 886 1517",
        "email": "cynorsolutionsgroup@gmail.com",
        "contactType": "customer service",
        "availableLanguage": "es",
    },
    "sameAs": ["https://www.instagram.com/cynor_solutions"],
}


def asset_version():
    h = hashlib.sha1()
    for p in [ROOT / "css/cynor.css", ROOT / "js/cynor.js", ROOT / "js/blog.js", ROOT / "js/hero3d.js"]:
        h.update(p.read_bytes())
    return h.hexdigest()[:10]


def expand_includes(html, depth=0):
    def repl(m):
        name = m.group(1).strip()
        part = (TEMPLATES / "partials" / f"{name}.html").read_text(encoding="utf-8")
        return expand_includes(part, depth + 1)

    if depth > 4:
        raise RuntimeError("includes demasiado anidados")
    return re.sub(r"<!--\s*include:\s*([\w-]+)\s*-->", repl, html)


def read_meta(raw, name):
    m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", raw, re.S)
    if not m:
        raise RuntimeError(f"{name}: falta el bloque <!--meta ... -->")
    return json.loads(m.group(1)), raw[m.end():]


def build_page(src, base, version, raw=None, replacements=None):
    raw = raw if raw is not None else src.read_text(encoding="utf-8")
    meta, rest = read_meta(raw, src.name)
    body = expand_includes(rest)
    for marker, value in (replacements or {}).items():
        body = body.replace(marker, value)

    path = meta["path"]
    canonical = SITE + ("/" if path == "/" else path)
    graph = [{"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": "Cynor", "inLanguage": "es-CO"}, ORGANIZATION]
    graph += meta.get("schema", [])
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)

    out = base
    for key, value in {
        "title": meta["title"],
        "description": meta["description"],
        "canonical": canonical,
        "robots": '<meta name="robots" content="noindex">' if meta.get("noindex") else "",
        "nav": meta.get("nav", ""),
        "og_image": meta.get("og_image", OG_DEFAULT),
        "og_type": meta.get("og_type", "website"),
        "schema": schema,
        "extra_scripts": meta.get("scripts", ""),
        "asset_v": version,
        "body": body.rstrip(),
    }.items():
        out = out.replace("{{" + key + "}}", value)

    if "{{" in out:
        raise RuntimeError(f"{src.name}: quedó un marcador sin reemplazar")
    if "—" in out or "–" in out:
        raise RuntimeError(f"{src.name}: tiene rayas largas (— o –); usa guion normal")

    target = ROOT / meta.get("out", src.name)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return str(target.relative_to(ROOT)), canonical, meta.get("noindex", False)


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
WA_CALL = "https://wa.me/573128861517?text=Hola%20Cynor%2C%20quiero%20agendar%20una%20llamada%20de%2030%20minutos"


def fecha_larga(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} de {MESES[m - 1]} de {y}"


def load_posts():
    posts = []
    for f in sorted(POSTS_DIR.glob("*.html")):
        meta, body = read_meta(f.read_text(encoding="utf-8"), f.name)
        for key in ["titulo", "slug", "fecha", "categoria", "tipo", "resumen", "imagen"]:
            if key not in meta:
                raise RuntimeError(f"{f.name}: falta '{key}' en el bloque meta")
        if f.stem != meta["slug"]:
            raise RuntimeError(f"{f.name}: el nombre del archivo debe ser igual al slug ({meta['slug']})")
        if meta["tipo"] == "vlog" and "video" not in meta:
            raise RuntimeError(f"{f.name}: un vlog necesita 'video'")
        meta["body"] = body.strip()
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        meta["minutos"] = max(1, round(words / 200))
        posts.append(meta)
    posts.sort(key=lambda p: p["fecha"], reverse=True)
    return posts


def esc(text):
    return html.escape(text, quote=True)


def post_card(p):
    is_vlog = p["tipo"] == "vlog"
    badge = '<span class="post-card__play" aria-hidden="true"><i class="ph-fill ph-play"></i></span>' if is_vlog else ""
    action = "Ver vlog" if is_vlog else "Leer artículo"
    return f"""        <a class="post-card{' post-card--vlog' if is_vlog else ''}" href="/blog/{p['slug']}" data-tipo="{p['tipo']}">
          <div class="post-card__img"><img src="{p['imagen']}" alt="" width="480" height="480" loading="lazy">{badge}</div>
          <div class="post-card__body">
            <p class="post-card__meta mono">{esc(p['categoria'])} · {fecha_larga(p['fecha'])}</p>
            <h2>{esc(p['titulo'])}</h2>
            <p>{esc(p['resumen'])}</p>
            <span class="link-arrow">{action} <span class="circle"><i class="ph ph-arrow-right" aria-hidden="true"></i></span></span>
          </div>
        </a>"""


def post_page(p, posts):
    url = f"{SITE}/blog/{p['slug']}"
    is_vlog = p["tipo"] == "vlog"
    if is_vlog:
        lines = "".join(f"<li>{esc(t)}</li>" for t in p.get("transcripcion", []))
        media = f"""
          <div class="vlog">
            <div class="vlog__player">
              <video controls playsinline preload="metadata" poster="{p['imagen']}">
                <source src="{p['video']}" type="video/mp4">
              </video>
            </div>
            <div class="vlog__script">
              <p class="mono">Lo que dice Zyra en el video</p>
              <ol>{lines}</ol>
            </div>
          </div>"""
    else:
        media = f"""
          <figure class="post__img"><img src="{p['imagen']}" alt="" width="1200" height="675"></figure>"""
    related = [q for q in posts if q["slug"] != p["slug"]][:2]
    related_html = "\n".join(post_card(q) for q in related)
    body = f"""    <article class="post">
      <div class="container post__wrap">
        <nav class="post__crumbs mono" aria-label="Ruta"><a href="/blog">Blog</a><span aria-hidden="true">/</span><span>{esc(p['categoria'])}</span></nav>
        <p class="post__meta mono">{fecha_larga(p['fecha'])} · {'Vlog' if is_vlog else str(p['minutos']) + ' min de lectura'}</p>
        <h1 class="post__title">{esc(p['titulo'])}</h1>
        <p class="post__lead">{esc(p['resumen'])}</p>{media}
        <div class="prose post__body">
{p['body']}
        </div>
        <aside class="post__cta">
          <p class="post__cta-title">¿Quieres esto en tu negocio?</p>
          <p>Agenda una llamada gratis de 30 minutos y te decimos por dónde empezar.</p>
          <a class="btn btn--white" href="{WA_CALL}" target="_blank" rel="noopener" data-track="cta_llamada_blog">Agenda una llamada <i class="ph ph-arrow-right" aria-hidden="true"></i></a>
        </aside>
      </div>
    </article>
    <section class="section--tight post__more">
      <div class="container">
        <p class="h2">Sigue leyendo</p>
        <div class="posts posts--related">
{related_html}
        </div>
      </div>
    </section>"""
    image = SITE + p["imagen"]
    article = {
        "@type": "BlogPosting",
        "@id": url + "#post",
        "headline": p["titulo"],
        "description": p["resumen"],
        "image": image,
        "datePublished": p["fecha"],
        "dateModified": p.get("actualizado", p["fecha"]),
        "inLanguage": "es-CO",
        "mainEntityOfPage": url,
        "author": {"@id": f"{SITE}/#organization"},
        "publisher": {"@id": f"{SITE}/#organization"},
        "articleSection": p["categoria"],
    }
    if is_vlog:
        article["video"] = {
            "@type": "VideoObject",
            "name": p["titulo"],
            "description": p["resumen"],
            "thumbnailUrl": image,
            "uploadDate": p["fecha"],
            "contentUrl": SITE + p["video"],
            "duration": p.get("duracion", "PT30S"),
            "inLanguage": "es-CO",
        }
    crumbs = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog"},
            {"@type": "ListItem", "position": 3, "name": p["titulo"], "item": url},
        ],
    }
    title = p["titulo"] + " | Cynor"
    meta = {
        "title": title,
        "description": p["resumen"][:300],
        "path": f"/blog/{p['slug']}",
        "nav": "blog",
        "out": f"blog/{p['slug']}.html",
        "og_image": image,
        "og_type": "article",
        "schema": [article, crumbs],
    }
    return "<!--meta\n" + json.dumps(meta, ensure_ascii=False) + "\n-->\n" + body + "\n"


def main():
    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    version = asset_version()
    urls = []
    posts = load_posts()
    cards = "\n".join(post_card(p) for p in posts)
    for src in sorted(PAGES.glob("*.html")):
        name, canonical, noindex = build_page(src, base, version, replacements={"<!-- blog-list -->": cards})
        if not noindex:
            urls.append(canonical)
        print(f"  {src.name} -> {name}")
    for p in posts:
        src = POSTS_DIR / f"{p['slug']}.html"
        name, canonical, _ = build_page(src, base, version, raw=post_page(p, posts))
        urls.append(canonical)
        print(f"  blog: {p['slug']} -> {name}")

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(urls, key=lambda u: (u != SITE + "/", u)):
        sitemap.append(f"  <url><loc>{u}</loc></url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    print(f"  sitemap.xml ({len(urls)} urls), assets v={version}")


if __name__ == "__main__":
    main()
