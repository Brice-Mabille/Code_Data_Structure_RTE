import os
import shutil
import logging
import calendar
from collections import defaultdict
from datetime import date, timedelta

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

def assigner_semaines_du_mois(base_path):
    """
    Attribue une semaine du mois à chaque date au format (année, mois, jour).
    Chaque semaine commence le lundi, et on compte les semaines dans le mois (Semaine 1, 2, etc).
    """
    dates = get_date_from_name(base_path)
    semaines = []
    for y, m, d in dates:
        jour_date = date(y, m, d)
        # Trouver le jour du mois correspondant au premier lundi
        premier_jour_du_mois = date(y, m, 1)
        decalage = (premier_jour_du_mois.weekday() + 1) % 7  # 0 si lundi, 6 si dimanche
        numero_semaine = ((d + decalage - 1) // 7) + 1
        semaines.append(f"Semaine {numero_semaine}")
    return semaines

def creer_dossiers_semaines(base_path, semaines):
    """
    Crée un dossier 'Semaine X' dans base_path pour chaque semaine unique dans la liste.
    """
    semaines_uniques = sorted(set(semaines), key=lambda s: int(s.split()[1]))  # Trier par numéro

    for semaine in semaines_uniques:
        chemin_dossier = os.path.join(base_path, semaine)
        if not os.path.exists(chemin_dossier):
            os.makedirs(chemin_dossier)
            print(f"Créé : {chemin_dossier}")
        else:
            print(f"Existe déjà : {chemin_dossier}")


def move_folders_by_weeks_list(base_path, dates, semaines):
    """
    Déplace les dossiers dans le bon dossier 'Semaine X' en utilisant les listes dates et semaines associées.
    """
    if len(dates) != len(semaines):
        raise ValueError("Les listes dates et semaines doivent avoir la même longueur.")

    # Associer noms de dossiers à leurs dates (on suppose que l'ordre dans os.listdir est le même que dates)
    dossier_names = [name for name in os.listdir(base_path)
                     if os.path.isdir(os.path.join(base_path, name))
                     and not name.startswith("Semaine")]

    # Tri pour synchroniser l’ordre des dossiers avec l’ordre de la liste dates
    dossier_names.sort()  # suppose que leur ordre lexicographique correspond à l'ordre chronologique

    for i, folder_name in enumerate(dossier_names):
        semaine = semaines[i]
        folder_path = os.path.join(base_path, folder_name)
        week_folder_path = os.path.join(base_path, semaine)

        # Créer le dossier Semaine X s’il n’existe pas
        os.makedirs(week_folder_path, exist_ok=True)

        dest_path = os.path.join(week_folder_path, folder_name)
        shutil.move(folder_path, dest_path)
        print(f"{folder_name} déplacé vers {semaine}")

def get_jours_ouvres_par_semaine(annee: int, mois: int):
    """
    Regroupe les jours ouvrés (lundi à vendredi) du mois en fonction
    des semaines ISO du calendrier, numérotées par "Semaine X" du mois.

    La semaine commence le lundi, donc les jours ouvrés sont regroupés
    par semaine calendaire.
    """

    jours_ouvres_par_semaine = defaultdict(list)
    current_day = date(annee, mois, 1)
    
    # Trouver la semaine ISO du premier jour du mois
    semaine_debut = current_day.isocalendar()[1]

    while current_day.month == mois:
        if current_day.weekday() < 5:  # lundi=0, ... vendredi=4
            # numéro de semaine ISO dans l'année
            num_semaine_iso = current_day.isocalendar()[1]
            # Calculer semaine relative au mois
            semaine_relative = num_semaine_iso - semaine_debut + 1
            semaine = f"Semaine {semaine_relative}"
            jours_ouvres_par_semaine[semaine].append(current_day)
        current_day += timedelta(days=1)
    return jours_ouvres_par_semaine

def verifier_nombre_donnees(base_path, dates, semaines):
    """
    Vérifie à tout moment si chaque dossier 'Semaine X' contient le bon nombre de données.
    Affiche aussi le chemin complet du dossier concerné.
    """
    dates_par_semaine = defaultdict(list)
    for i, semaine in enumerate(semaines):
        dates_par_semaine[semaine].append(dates[i])

    logger.info("=== Vérification du contenu des dossiers Semaine X ===")
    
    # Extraire année et mois depuis le nom du dossier (ex: "Janvier_2025_neg")
    nom_mois = os.path.basename(base_path)
    parts = nom_mois.split('_')
    mois_str, annee_str = parts[0], parts[1]

    mois_map = {
        "Janvier": 1, "Février": 2, "Mars": 3, "Avril": 4, "Mai": 5, "Juin": 6,
        "Juillet": 7, "Août": 8, "Septembre": 9, "Octobre": 10, "Novembre": 11, "Décembre": 12
    }

    mois = mois_map.get(mois_str, 0)
    annee = int(annee_str)

    for i in range(1, 6):
        semaine = f"Semaine {i}"
        dossier_semaine = os.path.join(base_path, semaine)

        if not os.path.isdir(dossier_semaine):
            logger.warning(f"{dossier_semaine} n'existe pas.")
            continue
        jours_ouvres = get_jours_ouvres_par_semaine(annee, mois)
        
        nb_attendus = len(jours_ouvres.get(semaine, []))
        contenus = [f for f in os.listdir(dossier_semaine)
                    if os.path.isdir(os.path.join(dossier_semaine, f)) or os.path.isfile(os.path.join(dossier_semaine, f))]
        nb_present = len(contenus)

        # Affichage avec chemin
        if nb_present == nb_attendus:
            logger.info(f"{dossier_semaine} : {nb_present} données présentes ; attendu : {nb_attendus}.")
        elif nb_present < nb_attendus:
            logger.warning(f"{dossier_semaine} : {nb_present} données présentes ; il en manque {nb_attendus - nb_present}.")
        else:
            logger.warning(f"{dossier_semaine} : {nb_present} données présentes ; {nb_present - nb_attendus} données en trop.")

        if contenus:
            logger.info(f"Contenu : {', '.join(contenus)}")
        else:
            logger.info(f"{dossier_semaine} est vide.")




if __name__ == "__main__":
    base_path = input("Entrez le chemin du dossier : ").strip()
    #if os.path.isdir(base_path):
    dates = get_date_from_name(base_path)
    semaines = assigner_semaines_du_mois(base_path)
    
    creer_dossiers_semaines(base_path, semaines)
    move_folders_by_weeks_list(base_path, dates, semaines)

    verifier_nombre_donnees(base_path, dates, semaines)
    logger.info("Tri terminé et vérification des sous-dossiers effectuée !")
else:
    logger.error("Chemin invalide.")
