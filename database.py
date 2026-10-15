import streamlit as st
import json
from sqlalchemy import text

# Connexion Neon — Streamlit lit [connections.neon] depuis secrets.toml
conn = st.connection("neon", type="sql")


def _execute(sql: str, params: dict = None):
    """Exécute une requête d'écriture (INSERT/UPDATE/DELETE) via transaction."""
    engine = conn.engine
    with engine.begin() as connection:
        connection.execute(text(sql), params or {})


def init_db():
    """Tables créées manuellement dans Neon. Rien à faire ici."""
    pass


# ==================== DEVICES ====================

def add_device(data: dict):
    _execute(
        """INSERT INTO devices
        (categorie, marque, modele, annee, stockage, couleur, etat,
         prix_fcfa, prix_usd, description, photo_principale, photos, statut)
        VALUES (:categorie, :marque, :modele, :annee, :stockage, :couleur, :etat,
                :prix_fcfa, :prix_usd, :description, :photo_principale,
                :photos, :statut)""",
        {
            "categorie": data["categorie"],
            "marque": data["marque"],
            "modele": data["modele"],
            "annee": int(data["annee"]),
            "stockage": data.get("stockage", ""),
            "couleur": data.get("couleur", ""),
            "etat": data["etat"],
            "prix_fcfa": float(data["prix_fcfa"]),
            "prix_usd": float(data["prix_usd"]),
            "description": data["description"],
            "photo_principale": data["photo_principale"],
            "photos": json.dumps(data["photos"]),
            "statut": data.get("statut", "Disponible"),
        },
    )


def get_devices(statut=None):
    if statut:
        df = conn.query(
            "SELECT * FROM devices WHERE statut = :statut ORDER BY date_ajout DESC",
            params={"statut": statut},
            ttl=5,
        )
    else:
        df = conn.query(
            "SELECT * FROM devices ORDER BY date_ajout DESC",
            ttl=5,
        )
    return df.to_dict("records")


def update_device(device_id, data: dict):
    _execute(
        """UPDATE devices SET
            categorie = :categorie,
            marque = :marque,
            modele = :modele,
            annee = :annee,
            stockage = :stockage,
            couleur = :couleur,
            etat = :etat,
            prix_fcfa = :prix_fcfa,
            prix_usd = :prix_usd,
            description = :description,
            statut = :statut
        WHERE id = :id""",
        {
            "categorie": data["categorie"],
            "marque": data["marque"],
            "modele": data["modele"],
            "annee": int(data["annee"]),
            "stockage": data.get("stockage", ""),
            "couleur": data.get("couleur", ""),
            "etat": data["etat"],
            "prix_fcfa": float(data["prix_fcfa"]),
            "prix_usd": float(data["prix_usd"]),
            "description": data["description"],
            "statut": data["statut"],
            "id": int(device_id),
        },
    )


def delete_device(device_id):
    _execute("DELETE FROM devices WHERE id = :id", {"id": int(device_id)})


# ==================== CONTACTS ====================

def add_contact(data: dict):
    _execute(
        """INSERT INTO contacts (nom, email, whatsapp, message, device_id)
           VALUES (:nom, :email, :whatsapp, :message, :device_id)""",
        {
            "nom": data["nom"],
            "email": data["email"],
            "whatsapp": data["whatsapp"],
            "message": data["message"],
            "device_id": data.get("device_id"),
        },
    )


def get_contacts():
    df = conn.query("SELECT * FROM contacts ORDER BY date DESC", ttl=5)
    return df.to_dict("records")