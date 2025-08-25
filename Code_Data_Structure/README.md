# Structure des Données et Creation de Métadonnées Splashtop

## Description
Une fois les missions d'inspection des postes HVDC réalisées par MK4.2 de Ross Robotics, il est important de télécharger ces données pour pourvoir les structurer et les réutiliser facilement et efficacement. Sur Splashtop, logiciel donnant accès au bureau à distance, les données peuvent être téléchargées localement grâce à la fonctionnalité "Transfert de fichier". L'inspection téléchargée se présente comme ceci :

```
RTE_mission_neg_2024-11-27_10_40_11
```
 Ce dossier est constitué de 3 dossiers, un dossier "images" contenant les images prises par le robot, un dossier "logs" contenant les actions faites par le robot pendant la mission et un dossier "recordings" contenant l'enregistrement audio de la mission. 
 
 Voici l'architecture de la donnée :

 ```
📂 RTE_mission_neg_2024-11-27_10_40_11

│── 📂 images
│   ├── 📂 front_camera
│   ├── 📂 optical_camera     
│   ├── 📂 radiometric_camera
│       ├── IP2_IT_1.jpeg      
│       ├── IP2_IT_2.jpeg      
│       ├── IP2_IT_3.jpeg      
│   ├── 📂 rear_camera 
│   ├── 📂 uv_camera

│── 📂 logs
│   ├── inspection_diagnostics.csv

│── 📂 recordings
│   ├── microphone_IP10_IT_2.wav              

```

Ce projet permet d'extraire et de structurer les métadonnées des différents types de fichiers (images, logs, audio) à partir d'un dossier contenant toutes les données `RTE_mission_neg_2024-11-27_10_40_11`. 

Les métadonnées sont stockées dans des fichiers JSON pour une analyse ultérieure.

## Structure du projet
```
📂 Code_Data_Structure
│── 📂 modules
│   ├── log_parser.py          # Extraction des métadonnées des logs
│   ├── image_metadata.py      # Extraction des métadonnées des images
│   ├── audio_processor.py     # Extraction des métadonnées des fichiers audio
│── 📂 old
│   ├── organisation_semaine.py   # V1 Script pour organiser les données par semaine
│── 📂 Test_2Données
│   ├── Semaine 3
│   ├── Semaine 4
│── main.py                    # Script principal pour les métadonnées 
|── organisation_semaineV2.py    # V2 Script pour organiser les données par semaine
|── vérification_taille_data.py# Script pour vérifier la taille des données selon une donnée de référence
│── README.md                  # Documentation
│── requirements.txt           # Bibliothèques nécessaires pour executer le projet
```

## Utilisation

1. Téléchargez les données sur Splashtop

2. Placez toutes les données téléchargées dans le dossier nommé `Donnée_Splashtop` avec un tri préalable par mois.

3. Dans un terminal, dirigez vous à ce chemin `K:/CCOS/DRD/08-GESTION DES ACTIFS/AIRMI/20. AIR/14. Données/07. Metadonnées/Brice/Code_Data_Structure` pour executer le code.

4. Installez les bibliothèques comme recommandé dans le fichier [Requirements](./requirements.txt) avec la commande :
   ```sh
   pip install -r requirements.txt
   ```

5. Vous pouvez ensuite entrer la commande
   ```sh
   python main.py
   ```

6. Saisir le chemin de l'inspection. Voir l'exemple plus bas.

7. Si la structure du dossier est invalide, il le sera affiché dans le terminal et la commande
   ```sh
   python organisation_semaineV2.py
   ```
   doit être executé pour structurer le dossier par semaine et savoir si le bon nombre de données existe. Le nombre de donnée est décrit par semaine dans le fichier "log_organisation_semaine.txt".

   Il est préférable d'exécuter ce script lorsque les données ne sont pas triées pour bien comprendre le nombre de données manquantes ou non.

8. Une fois la structure faite, réaliser l'étape 5 pour que le script traite chaque donnée et génère des fichiers JSON contenant les métadonnées.

9. Pour pouvoir vérifier si une donnée est correctement téléchargée ou que l'inspection soit complète, exécutez 
```sh
python vérification_taille_data_V2.py
``` 
Ceci permettra de savoir quelle taille fait la donnée et si des fichiers sont manquants par rapport à une donnée complète de référence.

## Exemple

1. Executez la commande 
```sh
   python main.py
   ```
2. Saisir ce chemin : `K:/CCOS/DRD/08-GESTION DES ACTIFS/AIRMI/20. AIR/14. Données/07. Metadonnées/Brice/Code_Data_Structure/Test_2Données`

3. <u>Résultats</u> :
```
2025-04-04 14:32:01,050 - WARNING - Structure incorrecte. Exécutez d'abord le script de structuration.

2025-04-04 14:32:01,093 - INFO - Dossiers trouvés : {'RTE_mission_neg_2024-11-27_10_40_11', 'RTE_mission_neg_2024-11-20_21_56_48'}

2025-04-04 14:32:01,104 - ERROR - Structure invalide. Veuillez d'abord exécuter `organisation_semaineV2.py` pour organiser les données.
```

4. Executez 
   ```sh
   python organisation_semaineV2.py
   ```

5. <u>Résultats</u> :
```
2025-04-04 14:34:00,500 - WARNING -  K:/CCOS/DRD/08-GESTION DES ACTIFS/AIRMI/20. AIR/14. Données/07. Metadonnées/Brice/Code_Data_Structure/Test_2Données/Semaine 1 contient 0 sous-dossiers au lieu de 5.

2025-04-04 14:34:00,509 - WARNING -  K:/CCOS/DRD/08-GESTION DES ACTIFS/AIRMI/20. AIR/14. Données/07. Metadonnées/Brice/Code_Data_Structure/Test_2Données/Semaine 2 contient 0 sous-dossiers au lieu de 5.

2025-04-04 14:34:00,518 - WARNING -  K:/CCOS/DRD/08-GESTION DES ACTIFS/AIRMI/20. AIR/14. Données/07. Metadonnées/Brice/Code_Data_Structure/Test_2Données/Semaine 3 contient 1 sous-dossiers au lieu de 5.

2025-04-04 14:34:00,536 - WARNING -  K:/CCOS/DRD/08-GESTION DES ACTIFS/AIRMI/20. AIR/14. Données/07. Metadonnées/Brice/Code_Data_Structure/Test_2Données/Semaine 4 contient 1 sous-dossiers au lieu de 5.
```

6. Ré-executez avec le bon chemin de dossier
   ```sh
   python main.py
   
   K:/CCOS/DRD/08-GESTION DES ACTIFS/AIRMI/20. AIR/14. Données/07. Metadonnées/Brice/Code_Data_Structure/Test_2Données/neg/Décembre_2025_neg
   ```
7. <u>Résultats</u> : Les métadonnées ont été extraite et sauvegardé dans les fichiers JSON situés dans les dossiers `output`

8. Vérifiez si une donnée est correctement téléchargée ou que l'inspection soit complète, exécutez 
```sh
python vérification_taille_data_V2.py

K:/CCOS/DRD/08-GESTION DES ACTIFS/AIRMI/20. AIR/14. Données/07. Metadonnées/Brice/Code_Data_Structure/Test_2Données/Semaine 3/RTE_mission_neg_2024-11-20_21_56_48
``` 

9. <u>Résultats</u> : WARNING:__main__:Le dossier fait moins de 200 Mo. Vérification des fichiers manquants...
INFO:__main__:Tous les fichiers attendus sont présents.

## Fonctionnalités des modules 
- **Log Parser** : Extrait les informations des fichiers Excel dans `logs/`
- **Image Metadata** : Extrait les métadonnées des images dans `images/`
- **Audio Processor** : Analyse les fichiers `.wav` dans `recordings/`
- **Gestion automatique des dossiers** : Si un dossier `output` existe déjà, il est ignoré

## Résultats
Les métadonnées extraites sont sauvegardées sous forme de fichiers JSON dans les répertoires `output/`.

#### PS : Les données de Novembre_2024 à Juillet_2025 ont été extraite pour les missions pos et neg.

### <u>Infos Complémentaires </u>

Fichier word

Formation Splashtop
