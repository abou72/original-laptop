"""Accès à la base Neon (PostgreSQL) via st.connection.

Lectures : conn.query() (mises en cache). Écritures : session SQLAlchemy avec
commit explicite, puis le cache est vidé.
"""
from __future__ import annotations

import json
import logging

import pandas as pd
import streamlit as st
from sqlalchemy import text

log = logging.getLogger(__name__)

SCHEMA = """
CREATE TABLE IF NOT EXISTS devices (
    id SERIAL PRIMARY KEY,
    categorie TEXT,
    marque TEXT NOT NULL,
    modele TEXT NOT NULL,
    annee INTEGER,
    stockage TEXT,
    couleur TEXT,
    etat TEXT DEFAULT 'Occasion',
    prix_fcfa NUMERIC DEFAULT 0,
    prix_usd NUMERIC DEFAULT 0,
    description TEXT,
    photo_principale TEXT,
    photos JSONB DEFAULT '[]'::jsonb,
    statut TEXT DEFAULT 'Disponible',
    date_ajout TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    email TEXT,
    whatsapp TEXT,
    message TEXT,
    device_id INTEGER REFERENCES devices(id) ON DELETE SET NULL,
    date TIMESTAMPTZ DEFAULT now()
);
"""


def _db_url() -> str | None:
    """URL Neon des secrets, avec le pilote psycopg2 explicite.

    SQLAlchemy 2.1 choisit psycopg (v3) pour « postgresql:// » : on force
    psycopg2 pour éviter « No module named psycopg ».
    """
    try:
        url = st.secrets["connections"]["neon"]["url"]
    except Exception:
        return None
    for prefix in ("postgresql://", "postgres://"):
        if url.startswith(prefix):
            return "postgresql+psycopg2://" + url[len(prefix):]
    return url


def _conn():
    # pool_pre_ping / pool_recycle : Neon coupe les connexions inactives
    # (« SSL connection has been closed unexpectedly »), on les rouvre à la volée.
    kwargs = {"pool_pre_ping": True, "pool_recycle": 280}
    url = _db_url()
    if url:
        kwargs["url"] = url
    return st.connection("neon", type="sql", **kwargs)


def _records(df: pd.DataFrame) -> list[dict]:
    """DataFrame -> liste de dicts, NaN/NaT remplacés par None."""
    if df.empty:
        return []
    return df.astype(object).where(df.notna(), None).to_dict("records")


def _execute(*statements: tuple[str, dict]) -> None:
    """Exécute une ou plusieurs requêtes d'écriture dans une seule transaction."""
    with _conn().session as s:
        for sql, params in statements:
            s.execute(text(sql), params)
        s.commit()
    st.cache_data.clear()  # les listes mises en cache sont périmées


@st.cache_resource(show_spinner=False)
def _ensure_schema() -> bool:
    try:
        with _conn().session as s:
            for stmt in SCHEMA.split(";"):
                if stmt.strip():
                    s.execute(text(stmt))
            s.commit()
        return True
    except Exception:
        log.warning("Création du schéma ignorée", exc_info=True)
        return False


def init_db() -> None:
    """Crée les tables si elles n'existent pas (une seule fois par processus)."""
    _ensure_schema()


# ---------------------------------------------------------------- appareils
def get_devices(statut: str | None = None) -> list[dict]:
    if statut:
        df = _conn().query(
            "SELECT * FROM devices WHERE statut = :statut ORDER BY date_ajout DESC",
            params={"statut": statut}, ttl=30,
        )
    else:
        df = _conn().query("SELECT * FROM devices ORDER BY date_ajout DESC", ttl=30)
    return _records(df)


def _params(data: dict) -> dict:
    return {
        "categorie": data["categorie"],
        "marque": data["marque"].strip(),
        "modele": data["modele"].strip(),
        "annee": int(data["annee"]),
        "stockage": (data.get("stockage") or "").strip(),
        "couleur": (data.get("couleur") or "").strip(),
        "etat": data["etat"],
        "prix_fcfa": float(data["prix_fcfa"]),
        "prix_usd": float(data["prix_usd"]),
        "description": (data.get("description") or "").strip(),
        "statut": data.get("statut", "Disponible"),
    }


def add_device(data: dict) -> None:
    params = _params(data)
    params["photo_principale"] = data["photo_principale"]
    params["photos"] = json.dumps(data["photos"])
    _execute((
        """INSERT INTO devices
           (categorie, marque, modele, annee, stockage, couleur, etat,
            prix_fcfa, prix_usd, description, photo_principale, photos, statut)
           VALUES (:categorie, :marque, :modele, :annee, :stockage, :couleur, :etat,
                   :prix_fcfa, :prix_usd, :description, :photo_principale,
                   :photos, :statut)""",
        params,
    ))


def update_device(device_id, data: dict) -> None:
    params = _params(data)
    params["id"] = int(device_id)
    _execute((
        """UPDATE devices SET
               categorie = :categorie, marque = :marque, modele = :modele,
               annee = :annee, stockage = :stockage, couleur = :couleur,
               etat = :etat, prix_fcfa = :prix_fcfa, prix_usd = :prix_usd,
               description = :description, statut = :statut
           WHERE id = :id""",
        params,
    ))


def delete_device(device_id) -> None:
    # On détache d'abord les messages : la suppression ne doit pas échouer
    # si la table contacts a une clé étrangère sans ON DELETE SET NULL.
    p = {"id": int(device_id)}
    _execute(
        ("UPDATE contacts SET device_id = NULL WHERE device_id = :id", p),
        ("DELETE FROM devices WHERE id = :id", p),
    )


# ---------------------------------------------------------------- contacts
def add_contact(data: dict) -> None:
    _execute((
        """INSERT INTO contacts (nom, email, whatsapp, message, device_id)
           VALUES (:nom, :email, :whatsapp, :message, :device_id)""",
        {
            "nom": data["nom"].strip(),
            "email": (data.get("email") or "").strip(),
            "whatsapp": (data.get("whatsapp") or "").strip(),
            "message": data["message"].strip(),
            "device_id": data.get("device_id"),
        },
    ))


def get_contacts() -> list[dict]:
    df = _conn().query(
        """SELECT c.*, d.marque, d.modele
           FROM contacts c LEFT JOIN devices d ON d.id = c.device_id
           ORDER BY c.date DESC""",
        ttl=30,
    )
    return _records(df)
