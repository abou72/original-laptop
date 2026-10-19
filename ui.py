"""Composants d'interface partagés (HTML, formats, liens)."""
from __future__ import annotations

import html
import json
import unicodedata
from datetime import datetime
from urllib.parse import quote

import streamlit as st

import config as cfg
from cloudinary_helper import optimized
from styles import build_css

esc = html.escape

PLACEHOLDER = (
    "data:image/svg+xml;utf8,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'%3E"
    "%3Crect width='400' height='400' fill='%23E9E3F7'/%3E"
    "%3Ctext x='200' y='210' font-family='sans-serif' font-size='20' "
    "text-anchor='middle' fill='%235F5775'%3EPhoto bient%C3%B4t disponible%3C/text%3E%3C/svg%3E"
)

# Couleurs courantes -> pastille (ordre = priorité de recherche dans le texte)
COULEURS = {
    "noir": "#111114", "minuit": "#1B2230", "graphite": "#3C3C42", "gris": "#8A8A93",
    "titane": "#B9B4AA", "argent": "#D9DBE0", "blanc": "#F5F5F7", "creme": "#EFE7DA",
    "or": "#E6C98F", "dore": "#E6C98F", "rose": "#F4A6C1", "rouge": "#D93A3A",
    "orange": "#F08A2C", "jaune": "#F5C542", "vert": "#2E9E6B", "bleu": "#2F6FDB",
    "violet": "#8B5CF6", "marron": "#7B5A3C",
}

ICONS = {
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
    "truck": '<path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.2"/>',
    "user": '<circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.5 3-6 6-6s6 2.5 6 6M16 11l2 2 4-4"/>',
    "swap": '<path d="M4 8h14l-3-3M20 16H6l3 3"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
}


# ------------------------------------------------------------------ helpers
def fmt_int(n) -> str:
    """12345 -> '12 345' (espace fine insécable, usage français)."""
    try:
        return f"{int(round(float(n))):,}".replace(",", "\u202f")
    except (TypeError, ValueError):
        return "—"


def wa_link(message: str | None = None) -> str:
    url = f"https://wa.me/{cfg.WHATSAPP_NUM}"
    return f"{url}?text={quote(message)}" if message else url


def clean_phone(raw: str) -> str:
    return "".join(ch for ch in (raw or "") if ch.isdigit())


def pluriel(cat: str) -> str:
    return cat if cat.endswith("s") else f"{cat}s"


def couleur_hex(nom: str | None) -> str | None:
    if not nom:
        return None
    t = unicodedata.normalize("NFD", nom.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    for cle, hexa in COULEURS.items():
        if cle in t:
            return hexa
    return None


def parse_photos(dev: dict) -> list[str]:
    photos = dev.get("photos")
    if isinstance(photos, str):
        try:
            photos = json.loads(photos)
        except ValueError:
            photos = []
    photos = [p for p in (photos or []) if isinstance(p, str) and p]
    main = dev.get("photo_principale")
    if main and main not in photos:
        photos.insert(0, main)
    return photos


def _compact(s: str) -> str:
    """Supprime indentations et sauts de ligne : un seul bloc HTML pour Markdown."""
    return "".join(line.strip() for line in s.splitlines())


def md(s: str) -> None:
    st.markdown(f'<div class="vt">{_compact(s)}</div>', unsafe_allow_html=True)


def inject_css(admin: bool = False) -> None:
    st.markdown(f"<style>{build_css(admin)}</style>", unsafe_allow_html=True)


# ------------------------------------------------------------------ blocs
def nav_and_hero(brands: list[str]) -> None:
    wa = wa_link()
    initiales = "".join(w[0] for w in cfg.NOM_BOUTIQUE.split()[:2]).upper()
    brands_html = ""
    if brands:
        chips = "".join(f"<span>{esc(b)}</span>" for b in brands[:10])
        brands_html = f'<div class="brands rise d5"><b>En stock</b>{chips}</div>'
    md(f"""
    <div id="top" class="anchor"></div>
    <nav class="nav"><div class="nav-in">
      <a class="brand" href="#top" target="_self"><i>{esc(initiales)}</i>{esc(cfg.NOM_BOUTIQUE)}</a>
      <div class="nav-links">
        <a href="#catalogue" target="_self">Appareils</a>
        <a href="#pourquoi" target="_self">Pourquoi nous</a>
        <a href="#contact" target="_self">Contact</a>
      </div>
      <a class="btn btn-violet btn-sm" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    </div></nav>
    <header class="hero fb">
      <div class="hero-in">
        <div>
          <h1><span class="rise d1">Smartphones &amp; ordinateurs.</span><span class="rise d2 soft">100&nbsp;% originaux.</span></h1>
          <p class="lead rise d3">Neufs, d'occasion ou reconditionnés : chaque appareil est vérifié avant la vente, avec des prix clairs en FCFA et en USD.</p>
          <div class="hero-cta rise d4">
            <a class="btn btn-white" href="#catalogue" target="_self">Voir les appareils</a>
            <a class="btn btn-ghost" href="{wa}" target="_blank" rel="noopener">Écrire sur WhatsApp</a>
          </div>
        </div>
        <div class="stage rise d3" aria-hidden="true">
          <div class="laptop"><div class="lid"><div class="screen"><i class="w1"></i><i class="w2"></i><i class="w3"></i></div></div><div class="base"></div></div>
          <div class="phone"><div class="pscreen"><span class="island"></span><i class="p1"></i><i class="p2"></i></div></div>
          <span class="spec s1">Garanti original</span>
          <span class="spec s2">Prix en FCFA</span>
        </div>
      </div>
      {brands_html}
    </header>
    """)


def section_header(anchor: str, title: str, sub: str = "") -> None:
    sub_html = f'<p class="sub">{esc(sub)}</p>' if sub else ""
    md(f'<section class="sec"><div id="{anchor}" class="anchor"></div><h2>{esc(title)}</h2>{sub_html}</section>')


def device_card(dev: dict) -> str:
    titre = f"{dev['marque']} {dev['modele']}"
    vendu = dev.get("statut") == "Vendu"
    photos = parse_photos(dev)
    img = optimized(photos[0], 800) if photos else PLACEHOLDER
    etat = dev.get("etat") or ""
    tag_cls = {"Neuf": "tag tag-neuf", "Reconditionné": "tag tag-reco"}.get(etat, "tag")
    tag = f'<span class="{tag_cls}">{esc(etat)}</span>' if etat else ""
    sold = '<span class="sold">Vendu</span>' if vendu else ""

    chips = []
    if dev.get("stockage"):
        chips.append(f"<span>{esc(dev['stockage'])}</span>")
    if dev.get("couleur"):
        hexa = couleur_hex(dev["couleur"])
        dot = f'<i style="background:{hexa}"></i>' if hexa else ""
        chips.append(f"<span>{dot}{esc(dev['couleur'])}</span>")
    if dev.get("annee"):
        chips.append(f"<span>{int(dev['annee'])}</span>")

    fcfa = f"{fmt_int(dev.get('prix_fcfa'))} FCFA"
    usd = f"≈ {fmt_int(dev.get('prix_usd'))} USD"

    desc = esc(dev.get("description") or "").replace("\r", "").replace("\n", "<br>")
    desc_html = f"<p>{desc}</p>" if desc else ""
    extra = photos[1:7]
    thumbs = ""
    if extra:
        links = "".join(
            f'<a href="{esc(p)}" target="_blank" rel="noopener"><img src="{esc(optimized(p, 300))}" alt="{esc(titre)}" loading="lazy"></a>'
            for p in extra
        )
        thumbs = f'<div class="thumbs">{links}</div>'
    more = (
        f'<details class="more"><summary>Voir les détails</summary><div class="more-in">{desc_html}{thumbs}</div></details>'
        if (desc_html or thumbs) else ""
    )

    if vendu:
        cta = '<span class="btn btn-line btn-block" aria-disabled="true">Appareil vendu</span>'
    else:
        detail = " - ".join(x for x in (dev.get("stockage"), etat) if x)
        msg = (f"Bonjour {cfg.NOM_BOUTIQUE}, je suis intéressé par le {titre}"
               f"{f' ({detail})' if detail else ''} (réf. #{dev.get('id')})")
        cta = f'<a class="btn btn-wa btn-block" href="{wa_link(msg)}" target="_blank" rel="noopener">Contacter sur WhatsApp</a>'

    cat = f'<div class="cat">{esc(dev["categorie"])}</div>' if dev.get("categorie") else ""
    return (
        f'<article class="dev{" is-sold" if vendu else ""}">'
        f'<div class="dev-media"><img src="{esc(img)}" alt="{esc(titre)}" loading="lazy">{tag}{sold}</div>'
        f'<div class="dev-body">{cat}<h3>{esc(titre)}</h3><div class="chips">{"".join(chips)}</div>'
        f'<div class="price"><strong>{esc(fcfa)}</strong><span>{esc(usd)}</span></div>'
        f'{more}{cta}</div></article>'
    )


def render_grid(devices: list[dict]) -> None:
    md(f'<div class="grid">{"".join(device_card(d) for d in devices)}</div>')


def band() -> None:
    md(f"""
    <div class="band">
      <div><h2>Un ancien appareil à échanger ?</h2>
      <p>Possibilité d'échange selon conditions. Écrivez-nous avec le modèle et son état, nous vous répondons directement.</p></div>
      <a class="btn btn-white" href="{wa_link(f'Bonjour {cfg.NOM_BOUTIQUE}, je voudrais échanger mon ancien appareil.')}" target="_blank" rel="noopener">Proposer un échange</a>
    </div>
    """)


def why_and_steps() -> None:
    cells = "".join(
        f'<div class="cell"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[ic]}</svg><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for t, d, ic in cfg.ARGUMENTS
    )
    steps = "".join(
        f'<div class="st"><span class="n">0{i}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for i, (t, d) in enumerate(cfg.ETAPES, 1)
    )
    md(f"""
    <section class="sec"><div id="pourquoi" class="anchor"></div>
      <h2>Pourquoi {esc(cfg.NOM_BOUTIQUE)}</h2>
      <div class="bento">
        <div class="big"><strong>100&nbsp;%</strong><em>originaux</em>
          <p>Tous nos appareils sont vérifiés et garantis originaux. Nous les sélectionnons avec soin.</p></div>
        {cells}
      </div>
    </section>
    <section class="sec"><h2>Comment ça marche</h2><div class="steps">{steps}</div></section>
    """)


def contact_side() -> None:
    wa = wa_link()
    md(f"""
    <section class="sec contact-side"><div id="contact" class="anchor"></div>
      <h2>Une question ? Écrivez-nous.</h2>
      <p class="sub" style="margin-bottom:1.5rem">Un modèle précis en tête ? Dites-nous ce que vous cherchez, nous vous répondons directement.</p>
      <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">WhatsApp {esc(cfg.WHATSAPP_AFFICHE)}</a>
      <a class="btn btn-line" href="mailto:{esc(cfg.EMAIL_CONTACT)}">{esc(cfg.EMAIL_CONTACT)}</a>
    </section>
    """)


def footer() -> None:
    initiales = "".join(w[0] for w in cfg.NOM_BOUTIQUE.split()[:2]).upper()
    md(f"""
    <div class="foot fb"><div class="foot-in">
      <div><a class="brand" href="#top" target="_self"><i>{esc(initiales)}</i>{esc(cfg.NOM_BOUTIQUE)}</a>
        <p>{esc(cfg.BASELINE)}. Livraison rapide sur {esc(cfg.VILLE)} et environs.</p></div>
      <div><p>WhatsApp : <a href="{wa_link()}" target="_blank" rel="noopener">{esc(cfg.WHATSAPP_AFFICHE)}</a></p>
        <p>E-mail : <a href="mailto:{esc(cfg.EMAIL_CONTACT)}">{esc(cfg.EMAIL_CONTACT)}</a></p></div>
      <div><p><a href="Admin" target="_self">Espace admin</a></p></div>
    </div>
    <div class="big-word" aria-hidden="true">{esc(cfg.NOM_BOUTIQUE)}</div>
    <div class="copy">© {datetime.now().year} {esc(cfg.NOM_BOUTIQUE)} — {esc(cfg.BASELINE)}</div></div>
    """)
