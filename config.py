"""Configuration unique de la boutique (une seule source de vérité)."""

NOM_BOUTIQUE = "Original Laptop"
BASELINE = "Smartphones & Ordinateurs"
VILLE = "Ouagadougou"
WHATSAPP_NUM = "22675316729"          # format international, sans + ni espaces
WHATSAPP_AFFICHE = "+226 75 31 67 29"
EMAIL_CONTACT = "pik.joss@gmail.com"
CLOUDINARY_FOLDER = "original_laptop"
PAGE_SIZE = 9  # appareils affichés par « page » dans le catalogue

CATEGORIES = ["Téléphone", "Ordinateur"]
ETATS = ["Neuf", "Occasion", "Reconditionné"]

# (titre, texte, icône)
ARGUMENTS = [
    ("Appareils inspectés", "Chaque appareil est vérifié avant la vente.", "search"),
    ("Photos réelles", "Des photos transparentes de chaque appareil.", "camera"),
    ("WhatsApp direct", "Échangez directement avec nous pour un service rapide.", "chat"),
    ("Livraison rapide", f"Sur {VILLE} et environs.", "truck"),
    ("Prix clairs", "En FCFA et en USD, sans frais cachés.", "tag"),
    ("Accompagnement", "Un suivi personnalisé de votre achat.", "user"),
    ("Échange possible", "Selon conditions : parlez-nous de votre ancien appareil.", "swap"),
    ("Clients satisfaits", "Votre satisfaction passe avant tout.", "star"),
]

ETAPES = [
    ("Choisissez", "Parcourez les appareils neufs, d'occasion ou reconditionnés."),
    ("Écrivez-nous", "Un message WhatsApp suffit, nous répondons directement."),
    ("Recevez", f"Livraison rapide sur {VILLE} et environs."),
]
