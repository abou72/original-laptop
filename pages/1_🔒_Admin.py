import streamlit as st

# ⚠️ EN PREMIER
st.set_page_config(page_title="Admin — Original Laptop", page_icon="🔒", layout="wide")

from database import (
    init_db, get_devices, add_device, update_device, delete_device, get_contacts,
)
from cloudinary_helper import upload_image

init_db()

# ---- AUTH ----
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 Espace Admin — Original Laptop")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if pwd == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ Mot de passe incorrect")
    st.stop()

# ---- HEADER + DECONNEXION ----
c1, c2 = st.columns([4, 1])
with c1:
    st.title("🔒 Gestion Original Laptop")
with c2:
    if st.button("🚪 Déconnexion"):
        st.session_state.auth = False
        st.rerun()

tab1, tab2 = st.tabs(["📱 Appareils", "📩 Messages reçus"])

# ============ TAB APPAREILS ============
with tab1:
    with st.expander("➕ Ajouter un appareil", expanded=False):
        with st.form("add_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            categorie = c1.selectbox("Catégorie *", ["Téléphone", "Ordinateur"])
            marque = c2.text_input("Marque *", placeholder="Apple, Samsung, HP...")
            modele = c3.text_input("Modèle *", placeholder="iPhone 13, Galaxy S22...")

            c4, c5, c6 = st.columns(3)
            annee = c4.number_input("Année", 2010, 2030, 2023)
            stockage = c5.text_input("Stockage", placeholder="128 Go, 512 Go...")
            couleur = c6.text_input("Couleur", placeholder="Noir, Blanc...")

            c7, c8, c9 = st.columns(3)
            etat = c7.selectbox("État", ["Neuf", "Occasion", "Reconditionné"])
            prix_fcfa = c8.number_input("Prix FCFA *", 0.0, step=5000.0)
            prix_usd = c9.number_input("Prix USD *", 0.0, step=10.0)

            desc = st.text_area("Description")

            photos_files = st.file_uploader(
                "Photos (la 1ère sera la photo principale)",
                type=["jpg", "jpeg", "png", "webp"],
                accept_multiple_files=True,
            )

            submitted = st.form_submit_button("💾 Enregistrer", use_container_width=True)

            if submitted:
                if not marque or not modele:
                    st.error("Marque et modèle obligatoires.")
                elif not photos_files:
                    st.error("Ajoutez au moins une photo.")
                else:
                    with st.spinner("Upload des photos sur Cloudinary..."):
                        urls = []
                        for f in photos_files:
                            try:
                                urls.append(upload_image(f))
                            except Exception as e:
                                st.error(f"Erreur upload {f.name}: {e}")

                    if urls:
                        add_device({
                            "categorie": categorie,
                            "marque": marque,
                            "modele": modele,
                            "annee": annee,
                            "stockage": stockage,
                            "couleur": couleur,
                            "etat": etat,
                            "prix_fcfa": prix_fcfa,
                            "prix_usd": prix_usd,
                            "description": desc,
                            "photo_principale": urls[0],
                            "photos": urls,
                            "statut": "Disponible",
                        })
                        st.success("✅ Appareil ajouté !")
                        st.rerun()

    st.divider()
    st.subheader("📋 Appareils existants")

    devices = get_devices()
    if not devices:
        st.info("Aucun appareil pour le moment.")
    else:
        for dev in devices:
            emoji = "❌" if dev["statut"] == "Vendu" else "✅"
            titre = f"{emoji} {dev['marque']} {dev['modele']} — #{dev['id']}"
            with st.expander(titre):
                c1, c2 = st.columns([1, 2])
                with c1:
                    if dev["photo_principale"]:
                        st.image(dev["photo_principale"], use_container_width=True)
                with c2:
                    statut = st.selectbox(
                        "Statut",
                        ["Disponible", "Vendu"],
                        index=0 if dev["statut"] == "Disponible" else 1,
                        key=f"st_{dev['id']}",
                    )
                    desc = st.text_area(
                        "Description",
                        dev["description"] or "",
                        key=f"desc_{dev['id']}",
                    )
                    c3, c4 = st.columns(2)
                    prix_fcfa = c3.number_input(
                        "Prix FCFA",
                        value=float(dev["prix_fcfa"] or 0),
                        key=f"pf_{dev['id']}",
                    )
                    prix_usd = c4.number_input(
                        "Prix USD",
                        value=float(dev["prix_usd"] or 0),
                        key=f"pu_{dev['id']}",
                    )

                    b1, b2 = st.columns(2)
                    if b1.button("💾 Mettre à jour", key=f"up_{dev['id']}",
                                 use_container_width=True):
                        d = dict(dev)
                        d.update({
                            "statut": statut,
                            "description": desc,
                            "prix_fcfa": prix_fcfa,
                            "prix_usd": prix_usd,
                        })
                        update_device(dev["id"], d)
                        st.success("✅ Mis à jour")
                        st.rerun()

                    if b2.button("🗑️ Supprimer", key=f"del_{dev['id']}",
                                 use_container_width=True):
                        delete_device(dev["id"])
                        st.warning("🗑️ Supprimé")
                        st.rerun()

# ============ TAB MESSAGES ============
with tab2:
    st.subheader("📩 Messages reçus")
    contacts = get_contacts()
    if not contacts:
        st.info("Aucun message pour le moment.")
    else:
        for ct in contacts:
            with st.expander(f"👤 {ct['nom']} — {ct['date']}"):
                st.write(f"**Email** : {ct['email']}")
                st.write(f"**WhatsApp** : {ct['whatsapp']}")
                st.write(f"**Appareil ID** : {ct['device_id']}")
                st.write(f"**Message** : {ct['message']}")
                if ct["whatsapp"]:
                    wa_link = (
                        f"https://wa.me/"
                        f"{ct['whatsapp'].replace('+','').replace(' ','')}"
                    )
                    st.link_button("📱 Répondre sur WhatsApp", wa_link)