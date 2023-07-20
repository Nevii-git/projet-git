==================================================================
			VERSION 0.4
==================================================================
                          _ _          
 ___  ___  ___ _   _ _ __(_) |_ _   _  
/ __|/ _ \/ __| | | | '__| | __| | | | 
\__ \  __/ (__| |_| | |  | | |_| |_| | 
|___/\___|\___|\__,_|_|  |_|\__|\__, | 
                                |___/  
  __                                   
 / _| ___  _ __                        
| |_ / _ \| '__|                       
|  _| (_) | |                          
|_|  \___/|_|                          
                                       
      _           _                    
  ___| |__   __ _| |_                  
 / __| '_ \ / _` | __|                 
| (__| | | | (_| | |_                  
 \___|_| |_|\__,_|\__|                 
                                       
					by ROUABAH Mohamed-Amine
==================================================================

==================================================================


********************** PATCH ************************

++++++++Error 1:    signe étrange au début du fichier json

            PATCHED
                    Une erreur est survenue lors du déchiffrement d'un fichier chiffré.
                    Le fichier json récupéré présentait un signe étrange au début du fichier
                    qui n'était pas présent dans le fichier d'origine.
            SOLUTION
                    Suppression de la ligne d'en-tête dans le fichier d'origine
                    et ajout de 6 lignes d'en-tête dans le fichier d'origine


++++++++Error 2:    lignes vides dans le fichier JSON déchiffré

            PATCHED
                    Lors du déchiffrement d'un fichier chiffré, des lignes vides étaient présentes
                    dans le fichier JSON déchiffré, ce qui altérait sa structure.
            SOLUTION
                    Utilisation de la fonction json.loads pour charger le contenu JSON déchiffré.
                    Utilisation de la fonction json.dumps avec les paramètres indent=4 et separators=(',', ': ')
                    pour formater le JSON avec une indentation et des séparateurs clairs.

++++++++Error 3:    dédoublement du JSON et du fichier ZIP lors du téléchargement
            PATCHED
                    Lors du téléchargement du fichier déchiffré, à la fois le JSON déchiffré et le fichier ZIP
                    étaient téléchargés, créant ainsi un dédoublement indésirable.
            SOLUTION
                    Modifier la fonction de téléchargement pour renvoyer uniquement le fichier ZIP.
                    Supprimer les lignes de code relatives au téléchargement du JSON déchiffré.


++++++++Error 4: Erreurs d'encodage des caractères spéciaux
            PATCHED
                Une erreur d'encodage s'est produite lors du traitement des caractères spéciaux,
                ce qui a entraîné leur affichage incorrect dans le fichier déchiffré.
            SOLUTION
                Création la fonction `before_encrypt` qui lit le fichier json et corrige
                les caractères spéciaux qui sont mal encodés.
                    

*****************************************************

Ce fichier README fournit des informations sur les fichiers présents dans le répertoire actuel.

LES FICHIERS:

    app.py
        Ce fichier contient le programme principal pour le chiffrement et le déchiffrement de fichiers. Il utilise l'algorithme AES (Advanced Encryption Standard)
        en mode CBC (Cipher Block Chaining) pour chiffrer et déchiffrer les fichiers. L'interface web est créée à l'aide du framework Flask.
        Ce fichier contient les routes et les fonctions nécessaires pour chiffrer et déchiffrer les fichiers.

    templates/index.html
        Ce fichier HTML contient la structure de la page web pour l'interface utilisateur.
         Il comprend un formulaire permettant à l'utilisateur de sélectionner un fichier à chiffrer ou déchiffrer.

INSTALLATIONS:

    Assurez-vous d'avoir les dépendances requises installées, telles que Flask, Crypto et zipfile.
    Vous pouvez les installer en utilisant pip, par exemple :

        pip install flask pycryptodome

Placez les fichiers `app.py` et `index.html` dans le même répertoire.

Exécutez le fichier `app.py` en exécutant la commande suivante dans votre terminal :

    python app.py

Ouvrez votre navigateur et accédez à l'adresse `http://localhost:5000` pour accéder à l'interface utilisateur.


UTILISATION:

Chiffrement de fichier
- Sélectionnez un fichier en cliquant sur le bouton "Choisir un fichier".
- Cliquez sur le bouton "Chiffrer" pour chiffrer le fichier sélectionné.
- Le fichier chiffré sera téléchargé au format ZIP.

Déchiffrement de fichier
- Sélectionnez un fichier chiffré en cliquant sur le bouton "Choisir un fichier".
- Entrez le mot de passe approprié dans le champ "Mot de passe".
- Cliquez sur le bouton "Déchiffrer" pour déchiffrer le fichier sélectionné.
- Le fichier déchiffré sera téléchargé.

PERSONNALISATION:
Vous pouvez personnaliser ce programme selon vos besoins spécifiques en modifiant le fichier `app.py`. Par exemple, vous pouvez modifier les extensions de fichiers acceptées, ajouter des fonctionnalités supplémentaires, personnaliser le design de l'interface utilisateur, etc.


NOTE DE FIN:

Veuillez noter que ce programme est fourni à titre d'exemple et ne garantit pas la sécurité complète de vos données. Il est recommandé de consulter un expert en sécurité informatique ou de suivre les meilleures pratiques de sécurité pour garantir la protection adéquate de vos données sensibles.

Pour toute question ou assistance supplémentaire, veuillez contacter l'équipe de support à l'adresse e-mail suivante :
m.arouabah@hotmail.com
