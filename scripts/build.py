#!/usr/bin/env python3
"""Arma las páginas del sitio a partir de pages/*.html y templates/.

Cada archivo en pages/ empieza con un bloque de metadatos:

    <!--meta
    {"title": "...", "description": "...", "path": "/salud", "nav": "salud"}
    -->

y puede incluir piezas compartidas con <!-- include: nombre --> (templates/partials/nombre.html).
El resultado se escribe en la raíz del repo (salud.html, index.html, ...), que es lo que publica Cloudflare Pages.

Uso: python3 scripts/build.py
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
TEMPLATES = ROOT / "templates"
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
    for p in [ROOT / "css/cynor.css", ROOT / "js/cynor.js", ROOT / "js/blog.js"]:
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


def build_page(src, base, version):
    raw = src.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", raw, re.S)
    if not m:
        raise RuntimeError(f"{src.name}: falta el bloque <!--meta ... -->")
    meta = json.loads(m.group(1))
    body = expand_includes(raw[m.end():])

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
    target.write_text(out, encoding="utf-8")
    return target.name, canonical, meta.get("noindex", False)


def main():
    base = (TEMPLATES / "base.html").read_text(encoding="utf-8")
    version = asset_version()
    urls = []
    for src in sorted(PAGES.glob("*.html")):
        name, canonical, noindex = build_page(src, base, version)
        if not noindex:
            urls.append(canonical)
        print(f"  {src.name} -> {name}")

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in sorted(urls, key=lambda u: (u != SITE + "/", u)):
        sitemap.append(f"  <url><loc>{u}</loc></url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    print(f"  sitemap.xml ({len(urls)} urls), assets v={version}")


if __name__ == "__main__":
    main()
