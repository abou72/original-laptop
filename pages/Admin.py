import streamlit as st

st.set_page_config(page_title="Admin — Original Laptop", page_icon="🔒", layout="wide",
                   initial_sidebar_state="collapsed")

import hmac
import time

import config as cfg
import ui
from cloudinary_helper import delete_images, optimized, upload_image
from database import (add_device, delete_device, get_contacts, get_devices,
                      init_db, update_device)

MAX_TRIES, LOCK_SECONDS = 5, 60

init_db()
ui.inject_css(admin=True)


# ---------------------------------------------------------------- AUTH
def check_password(pwd: str) -> bool:
    expected = st.secrets.get("ADMIN_PASSWORD")
    return bool(expected) and hmac.compare_digest(pwd.encode(), str(expected).encode())


if not st.session_state.get("auth"):
    st.markdown("## Espace admin")
    if "ADMIN_PASSWORD" not in st.secrets:
        st.error("ADMIN_PASSWORD n'est pas défini dans les secrets Streamlit.")
        st.stop()
    wait = st.session_state.get("lock_until", 0) - time.time()
    if wait > 0:
        st.warning(f"Trop d'essais. Réessayez dans {int(wait) + 1} s.")
        st.stop()
    with st.form("login"):
        pwd = st.text_input("Mot de passe", type="password")
        ok = st.form_submit_button("Se connecter", type="primary")
    if ok:
        if check_password(pwd):
            st.session_state.auth, st.session_state.fails = True, 0
            st.rerun()
        st.session_state.fails = st.session_state.get("fails", 0) + 1
        if st.session_state.fails >= MAX_TRIES:
            st.session_state.lock_until = time.time() + LOCK_SECONDS
            st.session_state.fails = 0
        st.error("Mot de passe incorrect.")
    st.stop()

# ---------------------------------------------------------------- EN-TÊTE
h1, h2, h3 = st.columns([5, 1.3, 1.3])
h1.markdown(f"## Gestion {cfg.NOM_BOUTIQUE}")
h2.page_link("tel.py", label="Voir le site", icon=":material/arrow_back:")
if h3.button("Déconnexion", width="stretch"):
    st.session_state.auth = False
    st.rerun()

try:
    devices, contacts = get_devices(), get_contacts()
except Exception as e:
    st.error(f"Base de données inaccessible : {e}")
    st.stop()

m1, m2, m3 = st.columns(3)
m1.metric("Disponibles", sum(d["statut"] != "Vendu" for d in devices))
m2.metric("Vendus", sum(d["statut"] == "Vendu" for d in devices))
m3.metric("Messages reçus", len(contacts))

tab1, tab2 = st.tabs(["Appareils", "Messages reçus"])


def _idx(options: list, value) -> int:
    return options.index(value) if value in options else 0


# ---------------------------------------------------------------- APPAREILS
with tab1:
    with st.expander("Ajouter un appareil"):
        with st.form("add_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            categorie = c1.selectbox("Catégorie *", cfg.CATEGORIES)
            marque = c2.text_input("Marque *", placeholder="Apple, Samsung, HP…")
            modele = c3.text_input("Modèle *", placeholder="iPhone 13, Galaxy S22…")
            c4, c5, c6 = st.columns(3)
            annee = c4.number_input("Année", 2010, 2030, 2023)
            stockage = c5.text_input("Stockage", placeholder="128 Go, 512 Go…")
            couleur = c6.text_input("Couleur", placeholder="Noir, Blanc…")
            c7, c8, c9 = st.columns(3)
            etat = c7.selectbox("État", cfg.ETATS)
            prix_fcfa = c8.number_input("Prix FCFA *", 0.0, step=5000.0)
            prix_usd = c9.number_input("Prix USD *", 0.0, step=10.0)
            desc = st.text_area("Description")
            files = st.file_uploader("Photos (la 1ère est la photo principale)",
                                     type=["jpg", "jpeg", "png", "webp"], accept_multiple_files=True)
            submitted = st.form_submit_button("Enregistrer", type="primary", width="stretch")

        if submitted:
            if not marque.strip() or not modele.strip():
                st.error("Marque et modèle obligatoires.")
            elif not files:
                st.error("Ajoutez au moins une photo.")
            else:
                urls, errors = [], []
                with st.spinner("Envoi des photos…"):
                    for f in files:
                        try:
                            urls.append(upload_image(f))
                        except Exception as e:
                            errors.append(f"{f.name} : {e}")
                for err in errors:
                    st.error(f"Échec de l'envoi — {err}")
                if urls and not errors:
                    add_device({"categorie": categorie, "marque": marque, "modele": modele,
                                "annee": annee, "stockage": stockage, "couleur": couleur,
                                "etat": etat, "prix_fcfa": prix_fcfa, "prix_usd": prix_usd,
                                "description": desc, "photo_principale": urls[0],
                                "photos": urls, "statut": "Disponible"})
                    st.success("Appareil ajouté.")
                    st.rerun()
                elif urls:
                    delete_images(urls)  # on n'enregistre pas une fiche incomplète
                    st.warning("Rien n'a été enregistré : corrigez l'erreur et réessayez.")

    st.subheader("Appareils existants")
    if not devices:
        st.info("Aucun appareil pour le moment.")
    for dev in devices:
        did = dev["id"]
        badge = "VENDU" if dev["statut"] == "Vendu" else "Disponible"
        with st.expander(f"{dev['marque']} {dev['modele']} — {badge} — #{did}"):
            ci, cf = st.columns([1, 2])
            photos = ui.parse_photos(dev)
            if photos:
                ci.image(optimized(photos[0], 500), width=320)
            with cf:
                a, b, c = st.columns(3)
                cats = cfg.CATEGORIES + ([dev["categorie"]] if dev["categorie"] not in cfg.CATEGORIES and dev["categorie"] else [])
                categorie_e = a.selectbox("Catégorie", cats, index=_idx(cats, dev["categorie"]), key=f"ca_{did}")
                marque_e = b.text_input("Marque", dev["marque"], key=f"ma_{did}")
                modele_e = c.text_input("Modèle", dev["modele"], key=f"mo_{did}")
                d1, d2, d3 = st.columns(3)
                annee_e = d1.number_input("Année", 2010, 2030, int(dev["annee"] or 2023), key=f"an_{did}")
                stock_e = d2.text_input("Stockage", dev["stockage"] or "", key=f"sk_{did}")
                coul_e = d3.text_input("Couleur", dev["couleur"] or "", key=f"co_{did}")
                e1, e2, e3, e4 = st.columns(4)
                etats = cfg.ETATS + ([dev["etat"]] if dev["etat"] not in cfg.ETATS and dev["etat"] else [])
                etat_e = e1.selectbox("État", etats, index=_idx(etats, dev["etat"]), key=f"et_{did}")
                fcfa_e = e2.number_input("Prix FCFA", value=float(dev["prix_fcfa"] or 0), step=5000.0, key=f"pf_{did}")
                usd_e = e3.number_input("Prix USD", value=float(dev["prix_usd"] or 0), step=10.0, key=f"pu_{did}")
                statuts = ["Disponible", "Vendu"]
                statut_e = e4.selectbox("Statut", statuts, index=_idx(statuts, dev["statut"]), key=f"st_{did}")
                desc_e = st.text_area("Description", dev["description"] or "", key=f"ds_{did}")

                b1, b2 = st.columns(2)
                if b1.button("Mettre à jour", key=f"up_{did}", type="primary", width="stretch"):
                    update_device(did, {"categorie": categorie_e, "marque": marque_e, "modele": modele_e,
                                        "annee": annee_e, "stockage": stock_e, "couleur": coul_e,
                                        "etat": etat_e, "prix_fcfa": fcfa_e, "prix_usd": usd_e,
                                        "description": desc_e, "statut": statut_e})
                    st.toast("Mis à jour")
                    st.rerun()
                confirm = b2.checkbox("Confirmer la suppression", key=f"cf_{did}")
                if st.button("Supprimer cet appareil", key=f"del_{did}", disabled=not confirm, width="stretch"):
                    delete_images(photos)
                    delete_device(did)
                    st.toast("Appareil supprimé")
                    st.rerun()

# ---------------------------------------------------------------- MESSAGES
with tab2:
    if not contacts:
        st.info("Aucun message pour le moment.")
    for ct in contacts:
        quand = ct["date"].strftime("%d/%m/%Y %H:%M") if hasattr(ct["date"], "strftime") else str(ct["date"])
        appareil = f"{ct['marque']} {ct['modele']}" if ct.get("marque") else "Demande générale"
        with st.expander(f"{ct['nom']} — {appareil} — {quand}"):
            if ct["email"]:
                st.write(f"**E-mail** : {ct['email']}")
            if ct["whatsapp"]:
                st.write(f"**WhatsApp** : {ct['whatsapp']}")
            st.write(ct["message"])
            num = ui.clean_phone(ct["whatsapp"])
            if num:
                st.link_button("Répondre sur WhatsApp", f"https://wa.me/{num}")
