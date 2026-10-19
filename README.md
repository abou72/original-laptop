# Original Laptop — site vitrine

Site Streamlit (une page + espace admin) : smartphones et ordinateurs, neufs, d'occasion ou reconditionnés.

## Lancer en local
1. `pip install -r requirements.txt`
2. Copier `.streamlit/secrets.toml.example` en `.streamlit/secrets.toml` et le remplir
3. `streamlit run tel.py`

Les tables `devices` et `contacts` sont créées automatiquement dans Neon si elles n'existent pas.

## Où modifier quoi
- `config.py` : nom, WhatsApp, e-mail, ville, catégories, arguments, étapes
- `styles.py` : couleurs et design (variables en haut du fichier)
- `ui.py` : composants HTML (hero, cartes, bento, pied de page)
- `tel.py` : page d'accueil — `pages/Admin.py` : espace admin (`/Admin`)

## Sécurité
Le mot de passe admin se définit dans les secrets (`ADMIN_PASSWORD`), jamais dans le code.
`.streamlit/secrets.toml` ne doit jamais être publié (il est dans `.gitignore`).
