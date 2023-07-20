"""
################################################################################
# Programme de chiffrement et déchiffrement de fichiers - Version 1.0
# Auteur: ROUABAH Mohamed-Amine
# Description: Ce programme utilise l'algorithme de chiffrement AES (Advanced
#              Encryption Standard) en mode CBC (Cipher Block Chaining) pour
#              chiffrer et déchiffrer des fichiers.
#              Il offre une interface web permettant à l'utilisateur de
#              sélectionner un fichier, de le chiffrer avec une clé générée
#              aléatoirement, de le stocker dans un fichier zip accompagné
#              d'un fichier texte contenant la clé, et de télécharger le fichier
#              zip. L'utilisateur peut également déchiffrer un fichier zip en
#              fournissant la clé appropriée, et télécharger le fichier
#              déchiffré.
# Chiffrement utilisé: AES (Advanced Encryption Standard)
# Mode de chiffrement: CBC (Cipher Block Chaining)
################################################################################
"""


"""
============================ NOTE DE PATCH ==================================

              _             _                    _       _
             | |           | |                  | |     | |
  _ __   ___ | |_ ___    __| | ___   _ __   __ _| |_ ___| |__
 | '_ \ / _ \| __/ _ \  / _` |/ _ \ | '_ \ / _` | __/ __| '_ \
 | | | | (_) | ||  __/ | (_| |  __/ | |_) | (_| | || (__| | | |
 |_| |_|\___/ \__\___|  \__,_|\___| | .__/ \__,_|\__\___|_| |_|
                                    | |
                                    |_|    version PATCH 1.0.1:



++++++++Error 1:    signe étrange au début du fichier json

            PATCHED
                    Une erreur est survenue lors du déchiffrement d'un fichier chiffré
                    le fichier json récupéré présentais un signe étrange au début du fichier
                    qui n'était pas présent dans le fichier d'origine.
            SOLUTION
                    suppression de la ligne d'en-tête dans le fichier d'origine
                    et ajout de 6 lignes d'en-tête dans le fichier d'origine
                    [l.82]      header_lines = b'\na\na\na\na\na\na\na\na\n\n'


    ========================================================================
    ========================================================================

++++++++Error 2:    lignes vides dans le fichier JSON déchiffré

            PATCHED
                    Lors du déchiffrement d'un fichier chiffré, des lignes vides étaient présentes
                    dans le fichier JSON déchiffré, ce qui altérait sa structure.
            SOLUTION
                    - Utilisation de la fonction json.loads pour charger le contenu JSON déchiffré.
                    - Utilisation de la fonction json.dumps avec les paramètres indent=4 et separators=(',', ': ')
                    pour formater le JSON avec une indentation et des séparateurs clairs.
                    [l.198]     decrypted_json = json.loads(decrypted_text)
                                formatted_json = json.dumps(
                                decrypted_json, indent=4, separators=(',', ': '))


    ========================================================================
    ========================================================================

++++++++Error 3:    dédoublement du JSON et du fichier ZIP lors du téléchargement
            PATCHED
                    Lors du téléchargement du fichier déchiffré, à la fois le JSON déchiffré et le fichier ZIP
                    étaient téléchargés, créant ainsi un dédoublement indésirable.
            SOLUTION
                    - Modifier la fonction de téléchargement pour renvoyer uniquement le fichier ZIP.
                    - Supprimer les lignes de code relatives au téléchargement du JSON déchiffré.
                    [l.78]      return send_file(zip_path, as_attachment=True)


    ========================================================================
    ========================================================================

++++++++Error 4: Erreurs d'encodage des caractères spéciaux
            PATCHED
                Une erreur d'encodage s'est produite lors du traitement des caractères spéciaux,
                ce qui a entraîné leur affichage incorrect dans le fichier déchiffré.
            SOLUTION
                Création la fonction `before_encrypt` qui lis le fichier json et corrige
                les caractères spéciaux qui sont mal encodés.
                    [l.190]         def before_encrypt(lines):
                                    equivalence_table = {
                                        'Ã©': 'é',
                                        'Ã¨': 'è',
                                        'Ãª': 'ê',
                                        'Ã«': 'ë',
                                        'Ã': 'à',
                                        'Ã¢': 'â',
                                        'Ã§': 'ç',
                                        'Ã®': 'î',
                                        'Ã¯': 'ï',
                                        'Ã´': 'ô',
                                        'Å': 'Œ',
                                        'Å“': 'œ',
                                        'Ã¹': 'ù',
                                        'Ã»': 'û',
                                        'Ã¼': 'ü',
                                        'Â°': '°',
                                        'â‚¬': '€',
                                        'Â£': '£',
                                        'Â§': '§',
                                        'Â©': '©',
                                        'Â®': '®',
                                        'â„¢': '™',
                                        # Ajoutez les autres caractères spéciaux ici
                                    }

                                    translation_table = str.maketrans(equivalence_table)

                                    translated_lines = [line.translate(translation_table) for line in lines]

                                    return ''.join(translated_lines)

"""

# =============================================================================


from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import tempfile
import shutil
import datetime
import zipfile
import json
app = Flask(__name__)

# Taille de la clé de chiffrement en bytes
KEY_SIZE = 32


@app.route('/')
def home():
    return render_template('index.html')


# =================== ENCRYPT ================================================
# Cette partie permet de chiffrer un fichier en utilisant l'algorithme AES avec
# une clé générée aléatoirement et de le stocker dans un fichier zip avec la
# clé de chiffrement.
# =============================================================================


@app.route('/encrypt', methods=['POST'])
def encrypt():
    file = request.files['file']

    if file:
        # Lire le contenu du fichier
        file_content = file.read()

        # Ajouter les 6 lignes d'en-tête afin de résoudre un bug lors du déchiffrement
        header_lines = b'\na\na\na\na\na\na\na\na\n\n'
        # header_lines = b''
        file_content = header_lines + file_content

        # Générer une clé de chiffrement aléatoire
        key = get_random_bytes(KEY_SIZE)

        # Initialiser le chiffreur AES en mode CBC avec la clé générée
        cipher = AES.new(key, AES.MODE_CBC)

        # Chiffrer le contenu du fichier
        encrypted_content = cipher.encrypt(pad(file_content))

        # Créer un fichier temporaire pour le fichier chiffré
        temp_file_path = os.path.join(tempfile.gettempdir(), 'encrypted_file')
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(encrypted_content)

        # Obtenir l'extension du fichier d'origine
        original_extension = os.path.splitext(file.filename)[1]

        # Créer le nom de fichier chiffré avec le même nom et l'extension .zip
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
        encrypted_filename = f"data-encrypted-{timestamp}.zip"

        # Créer le fichier zip
        zip_path = os.path.join(tempfile.gettempdir(), encrypted_filename)
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            # Ajouter le fichier chiffré au zip
            zip_file.write(temp_file_path, f"encrypted{original_extension}")

            # Ajouter le fichier txt contenant la clé au zip
            password_key = key.hex()
            zip_file.writestr("password key.txt", password_key)

        # Supprimer le fichier temporaire
        os.remove(temp_file_path)

        # Télécharger le fichier zip
        # downloads_folder = os.path.expanduser("~\Downloads")
        # downloads_path = os.path.join(downloads_folder, encrypted_filename)
        # shutil.move(zip_path, downloads_path)

        return send_file(zip_path, as_attachment=True)

    return 'Aucun fichier sélectionné.'


# =================== DECRYPT ================================================
# Cette partie permet de déchiffrer un fichier zip contenant un fichier chiffré
# ainsi qu'un fichier texte contenant la clé de chiffrement.
# =============================================================================

@app.route('/decrypt', methods=['POST'])
def decrypt():
    file = request.files['file']
    password = request.form['password']

    print(f"Mot de passe : {password}")

    if file:
        # Enregistrer le fichier zip
        zip_filename = secure_filename(file.filename)
        zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
        file.save(zip_path)

        # Ouvrir le fichier zip
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # Extraire le fichier chiffré
            encrypted_filename = None
            for name in zip_file.namelist():
                if name.startswith('encrypted'):
                    encrypted_filename = name
                    break
            if not encrypted_filename:
                return 'Fichier chiffré introuvable dans le fichier zip.'

            # Lire le contenu du fichier chiffré
            encrypted_content = zip_file.read(encrypted_filename)

            try:
                # Convertir le mot de passe hexadécimal en bytes
                password_bytes = bytes.fromhex(password)
            except ValueError:
                return 'Mot de passe invalide.'

            # Initialiser le chiffreur AES en mode CBC avec le mot de passe
            cipher = AES.new(password_bytes, AES.MODE_CBC)

            # Déchiffrer le contenu du fichier
            decrypted_content = cipher.decrypt(encrypted_content)

            # Supprimer le remplissage
            decrypted_content = unpad(decrypted_content)

            # Convertir le contenu déchiffré en une liste de lignes
            try:
                decrypted_text = decrypted_content.decode('utf-8')
            except UnicodeDecodeError:
                decrypted_text = decrypted_content.decode('latin-1')

            # Supprimer la première ligne et la remplacer par "{\n"
            decrypted_text = decrypted_text.split('\n', 1)[1]

            # Supprimer les lignes vides dans le JSON
            decrypted_json = json.loads(decrypted_text)
            formatted_json = json.dumps(
                decrypted_json, indent=4, separators=(',', ': '))

            # Créer un fichier temporaire pour le fichier déchiffré
            temp_file_path = os.path.join(
                tempfile.gettempdir(), 'decrypted_file')
            with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                temp_file.write(formatted_json)

            # Obtenir l'extension du fichier chiffré d'origine
            original_extension = os.path.splitext(encrypted_filename)[1]

            # Créer le nom de fichier déchiffré avec le même nom et l'extension d'origine
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
            decrypted_filename = f"data-decrypted-{timestamp}{original_extension}"

            # Renommer le fichier temporaire avec le nom déchiffré
            decrypted_file_path = os.path.join(
                tempfile.gettempdir(), decrypted_filename)
            if os.path.exists(decrypted_file_path):
                os.remove(decrypted_file_path)
            os.rename(temp_file_path, decrypted_file_path)

            # Télécharger le fichier déchiffré
            return send_file(decrypted_file_path, as_attachment=True)

        return 'Aucun fichier sélectionné.'

    return 'Aucun fichier sélectionné.'

# ==============================================================================

# Fonction de remplissage de bloc de chiffrement


def pad(data):
    length = AES.block_size - (len(data) % AES.block_size)
    padding = bytes([length]) * length
    return data + padding


# Fonction de suppression du remplissage
def unpad(data):
    return data[:-data[-1]]


# Fonction pour corriger les caractères spéciaux avant le téléchargement
def before_encrypt(lines):
    # Tableau d'équivalence pour les caractères spéciaux
    equivalence_table = {
        'Ã©': 'é',
        'Ã¨': 'è',
        'Ãª': 'ê',
        'Ã«': 'ë',
        'Ã': 'à',
        'Ã¢': 'â',
        'Ã§': 'ç',
        'Ã®': 'î',
        'Ã¯': 'ï',
        'Ã´': 'ô',
        'Å': 'Œ',
        'Å“': 'œ',
        'Ã¹': 'ù',
        'Ã»': 'û',
        'Ã¼': 'ü',
        'Â°': '°',
        'â‚¬': '€',
        'Â£': '£',
        'Â§': '§',
        'Â©': '©',
        'Â®': '®',
        'â„¢': '™',
        # Ajoutez les autres caractères spéciaux ici
    }

    # Créer une table de traduction à partir du tableau d'équivalence
    translation_table = str.maketrans(equivalence_table)

    # Remplacer les caractères spéciaux par leur équivalent
    for i in range(len(lines)):
        for char in equivalence_table:
            lines[i] = lines[i].replace(char, equivalence_table[char])

    return ''.join(lines)

# ================= MAIN ============================================


if __name__ == '__main__':
    app.run(debug=True)
