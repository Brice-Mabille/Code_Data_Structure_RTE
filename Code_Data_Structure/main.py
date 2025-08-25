import os
import logging
from modules.log_parser import parse_logs
from modules.image_metadata import ImageMetadata, process_images_in_folder
from modules.audio_processor import AudioProcessor, process_audio

logging.basicConfig(
    level=logging.INFO,  # Niveau des logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format du message
    handlers=[
        logging.FileHandler("log_métadonnée.txt"),  # Enregistre les logs dans un fichier
        logging.StreamHandler()  # Affiche les logs dans le terminal
    ]
)

logger = logging.getLogger(__name__)  # Création du logger

EXPECTED_WEEKS = {"Semaine 1", "Semaine 2", "Semaine 3", "Semaine 4", "Semaine 5"}
    
def is_correctly_structured(folder_path):
    """Vérifie si le dossier contient au moins un des dossiers de semaine attendus"""
    if not os.path.isdir(folder_path):
        logger.error(f"Le chemin n'est pas un dossier valide : {folder_path}")
        return False

    found_folders = {name for name in os.listdir(folder_path)
                     if os.path.isdir(os.path.join(folder_path, name))}

    matching_weeks = EXPECTED_WEEKS.intersection(found_folders)

    if matching_weeks:
        logger.info(f"Structure partiellement correcte. Dossiers semaine trouvés : {matching_weeks}")
        return True
    else:
        logger.warning("Structure incorrecte : aucun dossier 'Semaine X' trouvé.")
        logger.info(f"Dossiers trouvés : {found_folders}")
        return False

def process_folder(folder_path):
    # Vérifier si le dossier donné en entrée est valide
    if not os.path.isdir(folder_path):
        logger.warning(f"Le chemin spécifié n'est pas un dossier valide: {folder_path}")
        return
    for i in os.listdir(folder_path): #Parcours des dossiers semaines
        subfolder_path = os.path.join(folder_path, i)

        # Parcours des sous-dossiers pour extraire les métadonnées
        for j in os.listdir(subfolder_path):
            rte_neg_path = os.path.join(subfolder_path, j)
            # Appel des fonctions pour traiter les logs, les images et les fichiers audio
            logger.info(f"[Success] Traitement du dossier: {rte_neg_path}")
            
            # Traiter les logs
            parse_logs(rte_neg_path)
            
            # Traiter les images
            process_images_in_folder(rte_neg_path)
            
            # Traiter l'audio
            process_audio(rte_neg_path)

if __name__ == "__main__":
    # Demander à l'utilisateur de spécifier le chemin du dossier
    folder_path = input("Veuillez entrer le chemin du dossier contenant les sous-dossiers 'RTE_neg' : ").strip()
    
    if is_correctly_structured(folder_path):
        process_folder(folder_path)  # Appeler la fonction pour traiter ce dossier
    else:
        logger.error("Structure invalide. Veuillez d'abord exécuter `organisation_semaine.py` pour organiser les données.")


