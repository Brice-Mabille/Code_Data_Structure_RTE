import os
import shutil
import logging
import calendar
from collections import defaultdict
from datetime import date

# Configuration du logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Création d'un handler pour écrire les logs dans un fichier
file_handler = logging.FileHandler('log_organisation_semaine.txt')
file_handler.setLevel(logging.INFO)

# Format des logs
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Ajout des handlers au logger
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def get_date_from_name(base_path):
    """Extrait le jour (JJ) du nom et retourne le numéro de la semaine."""
    dates = []
    for folder_name in os.listdir(base_path):
        parts = folder_name.split('_')
        if len(parts)>=4:
            date_part = parts[3]
            try:
                year, month, day = date_part.split('-')
                year = int(year)
                month = int(month)
                day = int(day)
                dates.append((year, month, day))
            except ValueError:
                continue
        else:
            continue
    return dates

def get_week_number_from_name(base_path):
    """Extrait le jour (JJ) du nom et retourne le numéro de la semaine."""
    dates = get_date_from_name(base_path)
    weeks = []
    for nb_dates in dates : 
        year, month, day = nb_dates
        if 1 <= day <= 7:
            weeks.append("Semaine 1")  # Ajoute à la liste
        elif 8 <= day <= 14:
            weeks.append("Semaine 2")
        elif 15 <= day <= 21:
            weeks.append("Semaine 3")
        elif 22 <= day <= 28:
            weeks.append("Semaine 4")
        else:
            weeks.append("Semaine 5")
    return weeks  # Retourne la liste de toutes les semaines
    
def compute_expected_week_distribution(base_path):
    """
    Calcule le nombre de jours ouvrés attendus dans chaque semaine du mois
    pour chaque (année, mois) présent dans les noms de dossier.
    """
    dates = get_date_from_name(base_path)
    all_distributions = {}

    for (year, month, _) in dates:
        key = f"{year}-{month:02d}"
        
        # Évite de recalculer pour le même mois/année
        if key in all_distributions:
            continue

        num_days = calendar.monthrange(year, month)[1]
        week_distribution = defaultdict(int)
        for day in range(1, num_days + 1):
            weekday = date(year, month, day).weekday()
            if weekday < 5:  # Lundi=0, Vendredi=4 (jours ouvrés uniquement)
                if 1 <= day <= 7:
                    week = "Semaine 1"
                elif 8 <= day <= 14:
                    week = "Semaine 2"
                elif 15 <= day <= 21:
                    week = "Semaine 3"
                elif 22 <= day <= 28:
                    week = "Semaine 4"
                else:
                    week = "Semaine 5"
                week_distribution[week] += 1
        all_distributions[key] = dict(week_distribution)
    return all_distributions

def create_week_folders(base_path, weeks_needed):
    """Crée uniquement les dossiers de semaine nécessaires."""
    for i in range(1, 6):
        week_name = f"Semaine {i}"
        if week_name in weeks_needed:
            os.makedirs(os.path.join(base_path, week_name), exist_ok=True)
            logger.info(f"Dossier {week_name} créé.")

def move_folders_by_week(base_path):
    """Déplace les sous-dossiers dans les bons dossiers 'Semaine X'."""
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path) and not folder_name.startswith("Semaine"):
            weeks = get_week_number_from_name(base_path)
            for week_folder in weeks:
                week_folder_path = os.path.join(base_path, week_folder)
                # Déplace le dossier dans la semaine appropriée
                dest_path = os.path.join(week_folder_path, folder_name)
                shutil.move(folder_path, dest_path)
                logger.info(f"{folder_name} déplacé vers {week_folder}")
                break  # Sort de la boucle après le premier déplacement pour éviter de déplacer le même dossier plusieurs fois
        else:
            continue

def check_week_folders(base_path):
    """Vérifie qu'il y a 5 sous-dossiers dans chaque dossier 'Semaine X'."""
    for i in range(1, 6):
        week_name = f"Semaine {i}"
        week_folder = os.path.join(base_path, week_name)
        if os.path.isdir(week_folder):
            subfolders = [f for f in os.listdir(week_folder) if os.path.isdir(os.path.join(week_folder, f))]
            expected_distribution = compute_expected_week_distribution(week_folder)
            expected_count = sum(month_data.get(week_name, 0) for month_data in expected_distribution.values())
            if len(subfolders) < expected_count:
                logger.warning(f" {week_folder} contient {len(subfolders)} sous-dossiers au lieu de {expected_count}.")
            else:
                logger.info(f" {week_folder} contient {len(subfolders)} sous-dossiers.")
        else:
            logger.warning(f" {week_folder} n'existe pas.")

if __name__ == "__main__":
    base_path = input("Entrez le chemin du dossier : ").strip()
    get_date_from_name(base_path)
    #if os.path.isdir(base_path):
    weeks_needed = get_week_number_from_name(base_path)
    create_week_folders(base_path, weeks_needed)
    move_folders_by_week(base_path)
    check_week_folders(base_path)
    logger.info("Tri terminé et vérification des sous-dossiers effectuée !")
else:
    logger.error("Chemin invalide.")
