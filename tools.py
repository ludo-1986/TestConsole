import json
import os
from pathlib import Path
import shutil
import sys

def get_base_dir() -> Path:
    """Retourne le dossier des assets statiques (lecture seule dans l'APK)"""
    return Path(__file__).parent.parent / "assets"

def get_data_dir() -> Path:
    """Retourne le dossier persistant et inscriptible officiel de Flet"""
    # Flet fournit automatiquement ce chemin sur mobile et desktop
    app_storage_data = os.getenv("FLET_APP_STORAGE_DATA")
    dev = sys.platform == "linux"
    
    if app_storage_data and not dev:
        data_path = Path(app_storage_data)
        data_path.mkdir(parents=True, exist_ok=True)
        return data_path
    
    # En développement local sur ton PC (Ubuntu)
    local_dir = Path(__file__).parent.parent / "assets"
    local_dir.mkdir(parents=True, exist_ok=True)
    return local_dir

# Initialisation des chemins
assets_dir = get_base_dir()
data_dir = get_data_dir()


# load a JSON file
def read_file(dir: str="data", file_name: str="config.json") -> dict|list[dict]|bool:
    
    """
        Lecture des fichiers Json
        
        dir : STR -> nom du dossier dans lequel se trouve le fichier
        file_name : STR -> nom du fichier source
        
        return : DICT | LIST -> Le contenu du fichier Json
    """
    
    # Si on lit des données utilisateur, on cherche dans le dossier de données persistant
    if dir in ["data", "imgdata"]:
        file_path = data_dir / dir / file_name
    else:
        file_path = assets_dir / dir / file_name
    
    try:
        with file_path.open("r", encoding="utf-8") as f:
            
            return json.load(f)
        
    except FileNotFoundError:
        return False
    
    
def save_file(data: dict|list|str, file_name: str, old: str|bool=False) -> tuple|None:
    """
        Sauvegarde des données dans un fichier JSON et copie des images
        
        data : 
            dict | list -> Les données à enregistrer 
            str -> chemin de l'image à copier
                return : if data == str:
                    (str|bool, str)
                    
        dir : str 
            -> nom du dossier dans lequel se trouve le fichier JSON
            -> nom du dossier dans lequel se copie l'image
            
        file_name : str -> nom du fichier de destination
        
    """
    
    if not isinstance(data, (dict, list)):
        # Sauvegarde de l'image dans le dossier persistant
        dir_path = data_dir / "imgdata" / file_name
        dir_path.parent.mkdir(parents=True, exist_ok=True)
        src_path = Path(data).resolve()
        shutil.copy(src_path, dir_path)
        message = "Pas d'ancienne image"
            
        if old:
            
            try:
                os.remove(os.path.join(data_dir, old))
                message = f"Image - {old.split('/')[-1]} - supprimée"
                
            except:
                message = f"Chemin : {old} introuvable !!!"
                
        return f"imgdata/{file_name}", message
            
    else:
        # Sauvegarde du JSON dans le dossier persistant
        file_path = data_dir / "data" / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
    
def validate_mandatory_fields(input_data: dict, fields_to_check: list[tuple[str, str]]) -> list[str]:
    """
    Vérifie une liste de champs obligatoires.
    :param input_data: Le dictionnaire contenant les données des champs.
    :param fields_to_check: Une liste de tuples (clé_du_champ, nom_affichable).
    :return: La liste des noms des champs qui sont vides.
    """
    missing_fields = []
    
    field = {
        "profile" : [
            ("first_name", "Prénom"),
            ("last_name", "Nom"),
            ("height", "Taille")
        ],
        "news" : [
            ("feel", "Humeur"),
            ("title", "Titre de la journée")
        ],
        "walking" : [
            ("title", "Titre"),
            ("feet", "Nombre de pas"),
            ("difficult", "Niveau de difficulté")
        ],
        "receipt" : [
            ("title", "Titre"),
            ("ingredient", "Liste des ingrédients"),
            ("description", "Description")
        ],
        "idea" : [
            ("title", "Titre"),
            ("description", "Description")
        ]
    }
    
    for key, label in field.get(fields_to_check):
        value = input_data.get(key)
        # On vérifie si la valeur est absente, None ou vide
        if not value or (isinstance(value, str) and not value.strip()):
            missing_fields.append(label)
    return missing_fields


def replace_char(word: str) -> str:
        replacements = str.maketrans({
            " ": "_", "/": "_", "'": "_", "\"": "_", ",": "_",
            "é": "e", "è": "e", "ê": "e", "ë": "e", "à": "a", "ç": "c"
        })
        return word.lower().translate(replacements)
