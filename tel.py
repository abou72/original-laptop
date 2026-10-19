import streamlit as st

# DOIT être la toute première commande Streamlit
st.set_page_config(
    page_title="Original Laptop — Smartphones & Ordinateurs à Ouagadougou",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

import logging
import re
import time

import config as cfg
import ui
from database import add_contact, get_devices, init_db

log = logging.getLogger(__name__)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TRIS = ["Plus récents", "Prix croissant", "Prix décroissant"]

init_db()
ui.inject_css()

try:
    devices = get_devices()
except Exception:
    log.exception("Chargement du catalogue impossible")
    devices = []
    st.warning("Le catalogue est momentanément indisponible. Contactez-nous sur WhatsApp en attendant.")

brands_in_stock = sorted({d["marque"] for d in devices if d["marque"] and d.get("statut") != "Vendu"})
ui.nav_and_hero(brands_in_stock)

# ------------------------------------------------------------ catalogue
ui.section_header("catalogue", "Nos appareils",
                  "Smartphones et ordinateurs neufs, d'occasion ou reconditionnés. Écrivez-nous sur WhatsApp pour réserver.")

if devices:
    presentes = {d["categorie"] for d in devices if d["categorie"]}
    cats = [c for c in cfg.CATEGORIES if c in presentes] + sorted(presentes - set(cfg.CATEGORIES))
    labels = {"Tous": f"Tous ({len(devices)})"}
    for c in cats:
        labels[c] = f"{ui.pluriel(c)} ({sum(d['categorie'] == c for d in devices)})"
    cat_f = st.pills("Catégorie", ["Tous"] + cats, default="Tous", key="cat_f",
                     format_func=labels.get, label_visibility="collapsed") or "Tous"

    marques = ["Toutes"] + sorted({d["marque"] for d in devices if d["marque"]})
    presents = {d["etat"] for d in devices if d["etat"]}
    etats = ["Tous"] + [e for e in cfg.ETATS if e in presents] + sorted(presents - set(cfg.ETATS))

    f1, f2, f3, f4 = st.columns([2.2, 1.2, 1.3, 1.4])
    q = f1.text_input("Rechercher", placeholder="Ex. iPhone 13, 128 Go, HP…").strip().lower()
    marque_f = f2.selectbox("Marque", marques)
    etat_f = f3.selectbox("État", etats)
    tri = f4.selectbox("Trier par", TRIS)

    def _texte(d):
        return " ".join(str(d.get(k) or "") for k in ("marque", "modele", "stockage", "couleur", "annee")).lower()

    filtered = [
        d for d in devices
        if (cat_f == "Tous" or d["categorie"] == cat_f)
        and (marque_f == "Toutes" or d["marque"] == marque_f)
        and (etat_f == "Tous" or d["etat"] == etat_f)
        and (not q or q in _texte(d))
    ]
    prix = lambda d: float(d.get("prix_fcfa") or 0)
    if tri == "Prix croissant":
        filtered.sort(key=prix)
    elif tri == "Prix décroissant":
        filtered.sort(key=prix, reverse=True)
    filtered.sort(key=lambda d: d.get("statut") == "Vendu")  # vendus en dernier (tri stable)

    # pagination : on repart de zéro dès que les filtres changent
    signature = (cat_f, q, marque_f, etat_f, tri)
    if st.session_state.get("sig") != signature:
        st.session_state.sig = signature
        st.session_state.shown = cfg.PAGE_SIZE
    shown = st.session_state.get("shown", cfg.PAGE_SIZE)

    if filtered:
        n = len(filtered)
        st.markdown(f'<div class="vt"><p class="count">{n} appareil{"s" if n > 1 else ""}</p></div>',
                    unsafe_allow_html=True)
        ui.render_grid(filtered[:shown])
        if n > shown:
            _, mid, _ = st.columns([1, 1, 1])
            if mid.button("Afficher plus d'appareils", width="stretch"):
                st.session_state.shown = shown + cfg.PAGE_SIZE
                st.rerun()
    else:
        ui.md('<div class="empty"><strong>Aucun appareil ne correspond.</strong>'
              'Modifiez les filtres ou écrivez-nous : nous cherchons le modèle que vous voulez.</div>')
else:
    ui.md('<div class="empty"><strong>Le catalogue se remplit.</strong>'
          'Écrivez-nous sur WhatsApp pour connaître les arrivages.</div>')

# ------------------------------------------------------------ échange / confiance / étapes
ui.band()
ui.why_and_steps()

# ------------------------------------------------------------ contact
left, right = st.columns([5, 6], gap="large")
with left:
    ui.contact_side()
with right:
    st.markdown('<div style="height:4.2rem"></div>', unsafe_allow_html=True)
    options = {"Autre / pas encore choisi": None}
    for d in devices:
        if d.get("statut") != "Vendu":
            label = f"{d['marque']} {d['modele']} {d.get('stockage') or ''} (#{d['id']})"
            options[" ".join(label.split())] = d["id"]
    with st.form("contact_form", clear_on_submit=True):
        nom = st.text_input("Votre nom *")
        c1, c2 = st.columns(2)
        email = c1.text_input("E-mail")
        wa = c2.text_input("WhatsApp", placeholder="+226 …")
        appareil = st.selectbox("Appareil concerné", list(options))
        message = st.text_area("Votre message *", height=110)
        envoyer = st.form_submit_button("Envoyer ma demande", type="primary", width="stretch")

    if envoyer:
        if not nom.strip() or not message.strip():
            st.error("Indiquez votre nom et votre message.")
        elif not email.strip() and not wa.strip():
            st.error("Laissez un e-mail ou un numéro WhatsApp pour que nous puissions vous répondre.")
        elif email.strip() and not EMAIL_RE.match(email.strip()):
            st.error("Cette adresse e-mail ne semble pas valide.")
        elif time.time() - st.session_state.get("last_contact", 0) < 20:
            st.warning("Votre demande vient d'être envoyée. Patientez quelques secondes avant d'en envoyer une autre.")
        else:
            try:
                add_contact({"nom": nom, "email": email, "whatsapp": wa,
                             "message": message, "device_id": options[appareil]})
                st.session_state.last_contact = time.time()
                st.success("Demande envoyée. Nous vous recontactons très vite.")
            except Exception:
                log.exception("Enregistrement du contact impossible")
                st.error("L'envoi a échoué. Écrivez-nous directement sur WhatsApp.")

ui.footer()
