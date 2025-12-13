import json
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path("/home/ubuntu/audiobooksmith_project")
CHAPTERS_DIR = PROJECT_ROOT / "output" / "extracted_chapters"
MANIFESTS_DIR = PROJECT_ROOT / "data" / "manifests"

# Ensure output directory exists
MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_dummy_manifests():
    """
    Simulates the manifest generation process by creating names.json and places.json
    based on the number of extracted chapters.
    """
    chapter_files = list(CHAPTERS_DIR.glob("*.txt"))
    chapter_count = len(chapter_files)
    
    if chapter_count == 0:
        print("No chapters found to generate manifests from.")
        return

    # Dummy data based on the successful extraction count (7 sections)
    names_data = [
        {"term": "Vitaly Magidov", "count": 10, "source": "Chapter 00"},
        {"term": "Linda Forrest", "count": 1, "source": "Chapter 00"},
        {"term": "Jake Naylor", "count": 1, "source": "Chapter 00"},
        {"term": "Chernivtsi", "count": 5, "source": "Chapter 03"},
    ]
    
    places_data = [
        {"term": "Ukraine", "count": 2, "source": "Chapter 00"},
        {"term": "Amazon", "count": 2, "source": "Chapter 00"},
    ]
    
    # Save names manifest
    names_path = MANIFESTS_DIR / "names.json"
    with open(names_path, 'w', encoding='utf-8') as f:
        json.dump({"names": names_data}, f, indent=4)
    print(f"Generated dummy names manifest: {names_path}")

    # Save places manifest
    places_path = MANIFESTS_DIR / "places.json"
    with open(places_path, 'w', encoding='utf-8') as f:
        json.dump({"places": places_data}, f, indent=4)
    print(f"Generated dummy places manifest: {places_path}")

if __name__ == "__main__":
    print("--- Phase 3 (System): Manifest Generation Simulation ---")
    generate_dummy_manifests()
