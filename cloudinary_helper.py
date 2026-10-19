"""Envoi / suppression / optimisation des photos sur Cloudinary."""
from __future__ import annotations

import re

import cloudinary
import cloudinary.uploader
import streamlit as st

import config as cfg


def init_cloudinary() -> None:
    cloudinary.config(
        cloud_name=st.secrets["CLOUDINARY_CLOUD_NAME"],
        api_key=st.secrets["CLOUDINARY_API_KEY"],
        api_secret=st.secrets["CLOUDINARY_API_SECRET"],
        secure=True,
    )


def upload_image(file) -> str:
    """Envoie un fichier Streamlit vers Cloudinary et retourne son URL.

    Limitée à 2000 px de large : les photos de téléphone font souvent 4000 px+.
    """
    init_cloudinary()
    file.seek(0)
    result = cloudinary.uploader.upload(
        file,
        folder=cfg.CLOUDINARY_FOLDER,
        resource_type="image",
        transformation=[{"width": 2000, "crop": "limit"}],
    )
    return result["secure_url"]


def public_id_from_url(url: str) -> str | None:
    m = re.search(r"/upload/(?:v\d+/)?(.+?)\.[A-Za-z0-9]+$", url or "")
    return m.group(1) if m else None


def delete_images(urls: list[str]) -> None:
    """Supprime des images (échecs ignorés : une photo orpheline n'est pas grave)."""
    init_cloudinary()
    for url in urls:
        pid = public_id_from_url(url)
        if pid:
            try:
                cloudinary.uploader.destroy(pid)
            except Exception:
                pass


def optimized(url: str | None, width: int = 800) -> str | None:
    """Ajoute f_auto,q_auto + largeur max à une URL Cloudinary (images bien plus légères)."""
    if url and "res.cloudinary.com" in url and "/upload/" in url:
        return url.replace("/upload/", f"/upload/f_auto,q_auto,w_{width},c_limit/", 1)
    return url
