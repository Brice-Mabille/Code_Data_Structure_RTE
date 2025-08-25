import os
import json
from PIL import Image
from PIL.ExifTags import TAGS
import logging

logger = logging.getLogger(__name__)

class ImageMetadata:
    def extract_metadata(self, image_path):
        """Extracts metadata from an image."""
        try:
            img = Image.open(image_path)
            exif_data = img._getexif()
                                            #Structure des métadonnées
            metadata = {
                "metadata obligatoire : "
                "FileName": os.path.basename(image_path),
                "Folder": os.path.dirname(image_path),
                "Filesize": round(os.path.getsize(image_path) / 1024, 2),  # KB
                "FileType": img.format,
                "FileTypeExtension": os.path.splitext(image_path)[1].upper(),
                "ImageSize": f"{img.size[0]}x{img.size[1]}",
                "DomaineActif": "station de conversion",
                "MoyenAcquisition": "Robot",
                "Prestataire": "Ross-Robotics",     #Modifiez ici certaines données pour la visualisation sur le json final
                "ModèleRobot": "MK4.2",
                "CM": "Toulouse",
                "GMR": "LARO",
                "GDP": "AUDE PO",
                "Site": "BAIXAS",
                "Localisation": os.path.basename(image_path).split("_")[0],
                "IdentifiantRéf-PosteElectrique": None,
            }
                                            #Extraction des métadonnées            
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == "Model":
                        metadata["Model"] = value
                    elif tag_name == "DateTimeOriginal":
                        metadata["DateTimeOriginal"] = value
                    elif tag_name == "ResolutionUnit":
                        metadata["ResolutionUnit"] = value
                    elif tag_name == "Humidity":
                        metadata["Humidity"] = f"{float(value)} %"
                    elif tag_name == "Pressure":
                        metadata["Pressure"] = f"{float(value)} Pa"
                    elif tag_name == "AmbientTemperature":
                        metadata["AmbientTemperature"] = f"{float(value)} °C"
            return metadata
        
        except Exception as e:
            logger.error(f"Error processing {image_path}: {e}")
            return None

    def save_metadata_to_json(self, metadata_list, output_path):
        """Saves extracted metadata to a JSON file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)        #Création du dossier output 
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(metadata_list, json_file, indent=4, ensure_ascii=False)   #Sauvegarde des données JSON


def process_images_in_folder(base_path):
    """Processes images in subfolders of the 'images' folder."""

    image = ImageMetadata()

    images_path = os.path.join(base_path, "images")
    output_path = os.path.join(images_path, "output")
        
    if not os.path.exists(images_path):
        logger.warning("No 'images' folder found.")
        return
    
    if os.path.exists(output_path):
        logger.warning("Output folder already exists. Process aborted.")
        return
        
    for folder in os.listdir(images_path):              #Vérification des sous dossiers dans 'images' donc les dossiers front_camera, optical_camera....
        folder_path = os.path.join(images_path, folder)
        if os.path.isdir(folder_path):
            metadata_list = []
                
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
                    metadata = image.extract_metadata(file_path)
                    if metadata:
                        metadata_list.append(metadata)
                
            if metadata_list:                              #Enregistrement des métadonnées
                json_output_path = os.path.join(output_path, f"{folder}.json")
                image.save_metadata_to_json(metadata_list, json_output_path)
                logger.info(f"[Success] Metadata saved: {json_output_path}")
            else:
                logger.warning(f" No images found in {folder}")

if __name__ == "__main__":
    base_folder = input("Enter the path to the RTE_neg folder: ").strip()
    process_images_in_folder(base_folder)
