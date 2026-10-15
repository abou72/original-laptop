import streamlit as st

st.set_page_config(
    page_title="À propos — Original Laptop",
    page_icon="ℹ️",
    layout="wide",
)

st.markdown("""
<style>
.section {
    background:#F5F3FF; padding:1.5rem; border-radius:12px;
    border-left:5px solid #7C3AED; margin-bottom:1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("ℹ️ À propos de Original Laptop")

st.markdown("""
### 🛍️ Qui sommes-nous ?

**Original Laptop** est votre boutique de confiance pour l'achat de
**smartphones et ordinateurs** neufs, d'occasion ou reconditionnés.

Nous sélectionnons chaque appareil avec soin, garantissons son authenticité
et vous proposons les meilleurs prix du marché.
""")

st.divider()
st.subheader("✨ Nos engagements")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class="section">
        <h3>✅ Authentique</h3>
        <p>Tous nos appareils sont vérifiés et garantis 100% originaux.</p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div class="section">
        <h3>💰 Meilleur prix</h3>
        <p>Des tarifs compétitifs, sans frais cachés, en FCFA et USD.</p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div class="section">
        <h3>📱 Contact direct</h3>
        <p>Échangez directement avec nous par WhatsApp pour un service rapide.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.subheader("🛡️ Pourquoi nous faire confiance ?")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - 🔍 **Appareils inspectés** avant vente
    - 📸 **Photos réelles** et transparentes
    - 💬 **Communication directe** par WhatsApp
    - 🚚 **Livraison rapide** sur Ouagadougou et environs
    """)
with col2:
    st.markdown("""
    - 💰 **Prix clairs**, en FCFA et USD
    - 🤝 **Accompagnement personnalisé**
    - 🔄 **Possibilité d'échange** selon conditions
    - ⭐ **Clients satisfaits** avant tout
    """)

st.divider()
st.subheader("📞 Nous contacter")
c1, c2 = st.columns(2)
with c1:
    st.link_button(
        "📱 WhatsApp — +226 75 31 67 29",
        "https://wa.me/22675316729",
        use_container_width=True,
    )
with c2:
    st.link_button(
        "✉️ Email",
        "mailto:pik.joss@gmail.com",
        use_container_width=True,
    )

st.divider()
st.caption("© Original Laptop — Smartphones & Ordinateurs")