import os
import json
import wave
import logging

logger = logging.getLogger(__name__)

class AudioProcessor:
    def extract_audio_metadata(self, audio_path):
        """Extract metadata from an audio file."""
        with wave.open(audio_path, 'rb') as wav_file:
            metadata = {                                #Structure des métadonnées
                "FileName": os.path.basename(audio_path),
                "Folder": os.path.dirname(audio_path),
                "Filesize": f"{os.path.getsize(audio_path) / 1024:.2f} KB",
                "Channels": wav_file.getnchannels(),
                "SampleRate": f"{wav_file.getframerate()} Hz",
                "BitDepth": f"{wav_file.getsampwidth() * 8} bits",
                "Duration": f"{wav_file.getnframes() / wav_file.getframerate():.2f} sec"
            }
        return metadata

    def save_audio_metadata_to_json(self, metadata, output_folder):
        """Save audio metadata to a JSON file."""
        os.makedirs(output_folder, exist_ok=True)           #Création du dossier output
        output_path = os.path.join(output_folder, "audio_metadata.json")
        with open(output_path, 'w', encoding='utf-8') as json_file:     #Sauvegarde des métadonnées
            json.dump(metadata, json_file, indent=4, ensure_ascii=False)
        logger.info(f"[Success] Metadata saved to {output_path}")

def process_audio(base_folder):
    """Process the audio file inside the recordings/ folder."""

    audio = AudioProcessor()

    recordings_folder = os.path.join(base_folder, "recordings")
    output_folder = os.path.join(recordings_folder, "output")
    
    if not os.path.exists(recordings_folder):
        logger.warning(" No recordings folder found.")
        return
        
    audio_files = [f for f in os.listdir(recordings_folder) if f.endswith(".wav")]
        
    if not audio_files:
        logger.warning(" No audio files found in recordings/.")
        return
        
    audio_path = os.path.join(recordings_folder, audio_files[0])  # Prend le premier fichier trouvé
    metadata = audio.extract_audio_metadata(audio_path)
    audio.save_audio_metadata_to_json(metadata, output_folder)

#if __name__ == "__main__":
 #   base_folder = input("Enter the path to the RTE_neg folder: ").strip()
  #  process_audio(base_folder)
