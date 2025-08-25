import os
import logging
from datetime import datetime

# --- Configuration du logger : terminal + fichier ---
log_filename = "inspection_verification.log"

# Création du handler fichier avec ajout automatique d'une ligne vide entre chaque exécution
file_handler = logging.FileHandler(log_filename, mode='a', encoding='utf-8')
stream_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[stream_handler, file_handler]
)

logger = logging.getLogger(__name__)

# --- Fonctions ---

def get_file_size_in_mb(file_path):
    """Retourne la taille d'un fichier en Mo."""
    return os.path.getsize(file_path) / (1024 * 1024)

def get_folder_size_in_mb(folder_path):
    """Retourne la taille totale d'un dossier (y compris sous-dossiers) en Mo."""
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                total_size += get_file_size_in_mb(file_path)
    return round(total_size, 2)

def get_files_in_folder(folder_path):
    """Retourne l'ensemble des chemins relatifs des fichiers dans un dossier (récursif)."""
    files = set()
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(full_path, folder_path)
            files.add(relative_path)
    return files

def compare_folders(reference_folder, target_folder):
    """Compare les fichiers entre deux dossiers et retourne ceux manquants dans le dossier cible."""
    ref_files = get_files_in_folder(reference_folder)
    tgt_files = get_files_in_folder(target_folder)

    missing_files = ref_files - tgt_files
    return missing_files

# --- Script principal ---

def main():
    target_folder = input("Entrez le chemin du dossier à vérifier : ").strip()
    reference_folder = "Z:/20. AIR/01. Ross-Robotics/Données_Splashtop/2024-2025/neg/Février_2025_neg/Semaine 4/RTE_mission_neg_2025-02-26_04_00_00"  # Dossier de référence à modifier si l'inspection évolue

    if not os.path.isdir(target_folder):
        logger.error(f"Le dossier cible n'existe pas : {target_folder}")
        return

    if not os.path.isdir(reference_folder):
        logger.error(f"Le dossier de référence n'existe pas : {reference_folder}")
        return

    # Étape 1 : Vérification de la taille
    folder_size = get_folder_size_in_mb(target_folder)
    logger.info(f"Taille du dossier cible : {folder_size} Mo")

    if folder_size >= 200:
        logger.info(" Le dossier semble complet (≥ 200 Mo). Aucune comparaison nécessaire.")
        return
    else:
        logger.warning(" Le dossier est incomplet (< 200 Mo). Comparaison avec la référence...")

    # Étape 2 : Comparaison des fichiers
    missing_files = compare_folders(reference_folder, target_folder)

    if not missing_files:
        logger.info(" Tous les fichiers attendus sont présents.")
    else:
        logger.warning(f"{len(missing_files)} fichiers manquants :")
        for f in sorted(missing_files):
            logger.warning(f"- {f}")

    with open(log_filename, 'a', encoding='utf-8') as f: #retour à la ligne dans le fichier .log
        f.write("\n\n")

# --- Point d'entrée ---
if __name__ == "__main__":
    main()
