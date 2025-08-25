import os
import logging

# Configuration du logger pour les messages d'erreur et de succès
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_file_size_in_mb(file_path):
    """Retourne la taille d'un fichier en Mo."""
    size = round(os.path.getsize(file_path) / (1024 * 1024), 2)
    return size

def check_folder_size(folder_path, min_size_mb=200):
    """Vérifie si la taille du dossier est supérieure à la taille minimale (200 Mo par défaut)."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            total_size += get_file_size_in_mb(os.path.join(dirpath, filename))
    
    logger.info(f"Le dossier fait {total_size} Mo.")
    return total_size >= min_size_mb

def get_files_in_folder(folder_path):
    """Retourne une liste de tous les fichiers dans un dossier, y compris les fichiers dans les sous-dossiers."""
    files = set()
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            files.add(os.path.relpath(os.path.join(dirpath, filename), folder_path))
    return files

def compare_folders(reference_folder, target_folder):
    """Compare les fichiers d'un dossier cible avec ceux d'un dossier de référence et retourne les fichiers manquants."""
    reference_files = get_files_in_folder(reference_folder)
    target_files = get_files_in_folder(target_folder)
    
    missing_files = reference_files - target_files
    return missing_files

def main():
    # Entrée du chemin du dossier de données
    target_folder = input("Veuillez entrer le chemin du dossier d'inspection (ex : RTE_mission_neg_2024-11-20_21_56_48) : ").strip()

    # Chemin du dossier de référence à spécifier ici
    reference_folder = "K:/CCOS/DRD/08-GESTION DES ACTIFS/AIRMI/20. AIR/14. Données/07. Metadonnées/Brice/Code_Data_Structure/Test_2Données/Semaine 4/RTE_mission_neg_2024-11-27_10_40_11"  # Dossier de référence
    # A modifier lorsque des données sont ajoutées dans une inspection : image optique par exemple

    # Vérification si le dossier d'inspection fait plus de 200 Mo
    if not check_folder_size(target_folder):
        logger.warning(f"Le dossier {target_folder} fait moins de 200 Mo. Vérification des fichiers manquants...")

        # Comparaison avec le dossier de référence
        missing_files = compare_folders(reference_folder, target_folder)
        print(missing_files)
        # Affichage des fichiers manquants
        if missing_files:
            logger.warning(f"Fichiers manquants dans {target_folder} :")
            for missing_file in missing_files:
                logger.warning(f"- {missing_file}")
        else:
            logger.info(f"Tous les fichiers attendus sont présents dans {target_folder}.")
    else:
        logger.info(f"Le dossier {target_folder} fait plus de 200 Mo. L'inspection est correcte.")

if __name__ == "__main__":
    main()
