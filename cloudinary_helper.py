import streamlit as st
import cloudinary
import cloudinary.uploader


def init_cloudinary():
    cloudinary.config(
        cloud_name=st.secrets["CLOUDINARY_CLOUD_NAME"],
        api_key=st.secrets["CLOUDINARY_API_KEY"],
        api_secret=st.secrets["CLOUDINARY_API_SECRET"],
        secure=True,
    )


def upload_image(file) -> str:
    init_cloudinary()
    result = cloudinary.uploader.upload(
        file,
        folder="original_laptop",
        resource_type="image",
    )
    return result["secure_url"]


def delete_image(public_id: str):
    init_cloudinary()
    cloudinary.uploader.destroy(public_id)