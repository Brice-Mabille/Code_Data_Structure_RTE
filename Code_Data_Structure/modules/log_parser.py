import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def parse_logs(logs_dir):
    """
    Parse log files (CSV) from a folder and save them as JSON in an 'output' folder.
    """
    logs_dir = logs_dir + "/logs"              #Modidication du chemin d'accès aux logs

    if not os.path.exists(logs_dir):
        logger.error(f" Error: The folder '{logs_dir}' does not exist.")
        return

    output_dir = os.path.join(logs_dir, "output")     # Création du dossier output dans logs_dir
    os.makedirs(output_dir, exist_ok=True)

    files_processed = 0

    for file in os.listdir(logs_dir):
        file_path = os.path.join(logs_dir, file)

        if file.endswith(".csv"):  # Vérifie que c'est bien un fichier CSV
            try:
                df = pd.read_csv(file_path)

                # Détection du type de fichier log
                if "Message" in df.columns:  # Inspection diagnostics
                    log_type = "inspection_diagnostics"
                elif "Unit" in df.columns:  # Sensor log
                    log_type = "sensor_log"
                else:
                    logger.warning(f" Skipping unrecognized log format: {file}")
                    continue

                # Génération du nom de fichier JSON
                json_filename = f"{file.replace('.csv', '')}.json"
                json_path = os.path.join(output_dir, json_filename)

                # Sauvegarde en JSON
                df.to_json(json_path, orient="records", indent=4)
                logger.info(f"[Success] Parsed and saved {file} -> {json_path}")

                files_processed += 1

            except Exception as e:
                logger.error(f" Error parsing {file}: {e}")

    if files_processed == 0:
        logger.warning(" No valid CSV files found in the folder.")

#if __name__ == "__main__":
 #   logs_path = input(" Enter the path to the file you want to get the metadata from Splashtop: ").strip()
  #  parse_logs(logs_path)