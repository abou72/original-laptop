import streamlit as st

# ⚠️ set_page_config DOIT être la 1ère commande Streamlit
st.set_page_config(
    page_title="Original Laptop — Smartphones & Ordinateurs",
    page_icon="📱",
    layout="wide",
)

import json
from database import init_db, get_devices, add_contact

init_db()

# ================== CONFIG ==================
WHATSAPP_NUM = "22675316729"
EMAIL_CONTACT = "pik.joss@gmail.com"
NOM_BOUTIQUE = "Original Laptop"
DEVISE_1 = "FCFA"
DEVISE_2 = "USD"
# ============================================

# ---- CSS personnalisé ----
st.markdown("""
<style>
.hero {
    background: linear-gradient(135deg, #7C3AED 0%, #A78BFA 100%);
    padding: 3rem 2rem; border-radius: 16px;
    text-align: center; margin-bottom: 2rem;
}
.hero h1 { color: #FFFFFF; font-size: 2.8rem; margin: 0; }
.hero p  { color: #F5F3FF; font-size: 1.2rem; margin-top: 0.5rem; }
.badge {
    display:inline-block; background:#FFFFFF; color:#7C3AED;
    padding:4px 12px; border-radius:20px; font-size:0.85rem;
    font-weight:bold; margin-bottom:10px;
}
.prix { color: #7C3AED; font-weight: bold; font-size: 1.3rem; }
</style>
""", unsafe_allow_html=True)

# ---- HERO ----
st.markdown(f"""
<div class="hero">
    <span class="badge">📱 SMARTPHONES & 💻 ORDINATEURS</span>
    <h1>{NOM_BOUTIQUE}</h1>
    <p>Votre prochain appareil, neuf ou occasion, au meilleur prix</p>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.link_button(
        "📱 WhatsApp — +226 75 31 67 29",
        f"https://wa.me/{WHATSAPP_NUM}",
        use_container_width=True,
    )
with c2:
    st.link_button(
        "✉️ Nous écrire",
        f"mailto:{EMAIL_CONTACT}",
        use_container_width=True,
    )

st.divider()

# ---- CATALOGUE ----
st.markdown("## 🛍️ Notre catalogue")

devices = get_devices()
if not devices:
    st.info("Aucun appareil disponible pour le moment. Revenez bientôt !")
    st.stop()

# Filtres
categories = ["Toutes"] + sorted({d["categorie"] for d in devices if d["categorie"]})
marques = ["Toutes"] + sorted({d["marque"] for d in devices if d["marque"]})
etats = ["Tous", "Neuf", "Occasion", "Reconditionné"]

f1, f2, f3 = st.columns(3)
with f1:
    cat_f = st.selectbox("Catégorie", categories)
with f2:
    marque_f = st.selectbox("Marque", marques)
with f3:
    etat_f = st.selectbox("État", etats)

filtered = [
    d for d in devices
    if (cat_f == "Toutes" or d["categorie"] == cat_f)
    and (marque_f == "Toutes" or d["marque"] == marque_f)
    and (etat_f == "Tous" or d["etat"] == etat_f)
]

# Grille
cols = st.columns(3)
for i, dev in enumerate(filtered):
    with cols[i % 3]:
        with st.container(border=True):
            img = dev["photo_principale"] or "https://via.placeholder.com/400x250?text=Original+Laptop"
            st.image(img, use_container_width=True)

            st.markdown(f"### {dev['marque']} {dev['modele']}")

            infos = []
            if dev.get("stockage"):
                infos.append(f"💾 {dev['stockage']}")
            if dev.get("couleur"):
                infos.append(f"🎨 {dev['couleur']}")
            if dev.get("annee"):
                infos.append(f"📅 {dev['annee']}")
            infos.append(dev["etat"])
            st.caption(" • ".join(infos))

            st.markdown(
                f"<p class='prix'>{dev['prix_fcfa']:,.0f} {DEVISE_1} "
                f"<small>(≈ {dev['prix_usd']:,.0f} {DEVISE_2})</small></p>",
                unsafe_allow_html=True,
            )

            if dev["statut"] == "Vendu":
                st.error("❌ VENDU")
            else:
                msg = (
                    f"Bonjour Original Laptop, je suis intéressé par le "
                    f"{dev['marque']} {dev['modele']} "
                    f"({dev.get('stockage','')} - {dev['etat']}) "
                    f"(réf. #{dev['id']})"
                )
                wa_url = f"https://wa.me/{WHATSAPP_NUM}?text={msg.replace(' ', '%20')}"
                st.link_button("📱 Contacter sur WhatsApp", wa_url, use_container_width=True)

            with st.expander("Voir plus / Demander info"):
                st.write(dev["description"] or "Pas de description.")

                photos = dev.get("photos")
                if isinstance(photos, str):
                    try:
                        photos = json.loads(photos)
                    except Exception:
                        photos = []
                if photos and len(photos) > 1:
                    st.write("**Autres photos :**")
                    for p in photos[1:]:
                        st.image(p, use_container_width=True)

                with st.form(f"contact_{dev['id']}"):
                    st.write("**Vous êtes intéressé ? Laissez vos coordonnées :**")
                    nom = st.text_input("Votre nom")
                    email = st.text_input("Email")
                    wa = st.text_input("WhatsApp")
                    msg2 = st.text_area("Message")
                    if st.form_submit_button("📩 Envoyer"):
                        add_contact({
                            "nom": nom,
                            "email": email,
                            "whatsapp": wa,
                            "message": msg2,
                            "device_id": dev["id"],
                        })
                        st.success("✅ Message envoyé ! Nous vous recontactons vite.")

st.divider()
st.caption(
    f"© {NOM_BOUTIQUE} — Smartphones & Ordinateurs • "
    f"WhatsApp : +226 75 31 67 29"
)