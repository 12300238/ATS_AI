"""
Utilitaire de conversion du fichier brut mock_data/raw/offre_mock.ndjson.

Ce fichier contient plusieurs objets JSON concaténés (sans séparateur ni
tableau englobant), avec un motif "offre complète" suivi d'un objet
"required_skills pondérés" pour la même offre. Ce script se contente
d'extraire chaque objet JSON individuellement et de les sauvegarder dans
un tableau — la réconciliation (associer les poids à la bonne offre,
inventer les champs manquants comme pour l'offre Cybersécurité) a été
faite manuellement pour produire mock_data/offers.json.

Utile si vous recevez d'autres fichiers du même format brut.

Usage :
    python scripts/convert_offre_mock.py
"""

import json
from pathlib import Path

RAW_PATH = Path(__file__).parent.parent / "mock_data" / "raw" / "offre_mock.ndjson"
OUT_PATH = Path(__file__).parent.parent / "mock_data" / "raw" / "offre_mock_parsed.json"


def parse_concatenated_json(text: str) -> list[dict]:
    """Extrait tous les objets JSON concaténés (avec ou sans saut de ligne)."""
    decoder = json.JSONDecoder()
    objects = []
    idx = 0
    length = len(text)
    while idx < length:
        # Avance jusqu'au prochain caractère non blanc
        while idx < length and text[idx].isspace():
            idx += 1
        if idx >= length:
            break
        obj, end = decoder.raw_decode(text, idx)
        objects.append(obj)
        idx = end
    return objects


def main() -> None:
    text = RAW_PATH.read_text(encoding="utf-8")
    objects = parse_concatenated_json(text)
    print(f"{len(objects)} objets JSON trouvés dans {RAW_PATH.name}")
    for i, obj in enumerate(objects):
        a_titre = "title" in obj
        print(f"  [{i}] {'offre complète' if a_titre else 'poids seuls'} "
              f"({len(obj.get('required_skills', []))} compétences)")
    OUT_PATH.write_text(json.dumps(objects, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"-> Sauvegardé dans {OUT_PATH}")


if __name__ == "__main__":
    main()
