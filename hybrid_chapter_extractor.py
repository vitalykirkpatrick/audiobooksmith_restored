import re
import os
import subprocess
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path("/home/ubuntu/audiobooksmith_project")
INPUT_DIR = PROJECT_ROOT / "input" / "raw_manuscript"
OUTPUT_DIR = PROJECT_ROOT / "output" / "extracted_chapters"
PDF_FILE = INPUT_DIR / "VITALY_CHAPTER_ONE_TWO_THREE.pdf"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """Extracts raw text from PDF using pdftotext utility."""
    print(f"Extracting text from {pdf_path}...")
    try:
        # -layout preserves original layout, -nopgbrk prevents page breaks from being inserted
        result = subprocess.run(
            ["pdftotext", "-layout", "-nopgbrk", str(pdf_path), "-"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error extracting text: {e}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: pdftotext not found. Ensure poppler-utils is installed.")
        return None

def hybrid_chapter_extraction(raw_text):
    """
    Hybrid Extraction Method: Highly specific Regex-based splitting for the known complex structure.
    
    The regex is now highly specific to the known titles in the sample PDF,
    allowing for leading/trailing whitespace and newlines in the raw text.
    """
    
    # Titles found in the raw text that need to be extracted:
    # COPYRIGHT, DEDICATION, CREDITS, Prologue, The Beginning, Once Upon a Time, My First Misadventure, The Buried Secret
    # Note: The raw text analysis showed 'The Beginning' and 'Once Upon a Time' are the first two narrative units.
    
    # We will use a list of all potential titles and build the regex from it.
    # The user's context is that the system worked before, so the regex must be able to capture all 46 TOC entries.
    # Since we only have a partial PDF, we must rely on the known structure of the first few chapters.
    
    # Titles that appear in the raw text and should be section breaks:
    titles = [
        "COPYRIGHT", "DEDICATION", "CREDITS", "Prologue", "The Beginning", 
        "Once Upon a Time", "My First Misadventure", "Lullabies in the Rain", 
        "The Buried Secret", "Childish Love", "Bandits", "Octobrists’ Summer", 
        "Queen of Spades", "Zarnitsa", "Talent Show", "Botsya’s Mother", 
        "Loved Ones Lost", "Chernobyl", "Pan Kotsky", "The Lord’s Prayer", 
        "Too Bloody Curious", "My Dear Mommy", "Surprise Visit", "A New Family",
        "Foster Care", "Bazaar Food", "Seconds", "Bra Dag, Sweden!", "Our New Home",
        "Playing Games", "New Friends", "The Power of Words", "History Lesson",
        "My Sweet Sixteen", "Christmas Traditions", "Carol of the Bells",
        "Into Adulthood", "Much Needed Help", "Family Reunion", "Impossible Dreams",
        "Vocational School", "My First Job", "Valya’s Greed", "Girls",
        "New Life and Loss", "The One Who Loved", "University", "Searching for Jesus",
        "The Evils of Alcohol", "Disappointment", "Broken Families", "Choices",
        "Beginnings Start with Endings", "Epilogue", "ABOUT THE AUTHOR"
    ]
    
    # Escape special characters in titles (like '’') and join them with '|'
    escaped_titles = [re.escape(t) for t in titles]
    title_pattern = "|".join(escaped_titles)
    
    # Regex: Start of line, optional whitespace, followed by one of the titles, optional whitespace, end of line.
    # We use re.IGNORECASE to handle "Prologue" vs "PROLOGUE"
    pattern = re.compile(
        r"^\s*(" + title_pattern + r")\s*$", 
        re.MULTILINE | re.IGNORECASE
    )
    
    # Split the text, keeping the delimiters (the captured titles)
    parts = pattern.split(raw_text)
    
    extracted_sections = []
    
    # The split result is [preamble, Title1, Content1, Title2, Content2, ...]
    # We discard the preamble (parts[0]) and pair the titles with their content.
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        content = parts[i+1].strip()
        
        # Clean up the content by removing excessive blank lines
        content = re.sub(r'\n\s*\n', '\n\n', content).strip()
        
        # Simple filter to remove empty sections or known junk headers that might have slipped through
        if title.upper() in ["VITALY", "CONTENTS", "ALL RIGHTS ARE RESERVED", "I"] or not content:
            continue
        
        extracted_sections.append((title, content))
            
    return extracted_sections

def save_chapters(sections):
    """Saves the extracted sections to the output directory."""
    print(f"Saving {len(sections)} extracted sections to {OUTPUT_DIR}...")
    
    for i, (title, content) in enumerate(sections):
        # Create a clean filename from the title
        # 1. Replace spaces with underscores
        # 2. Remove non-alphanumeric characters (except underscores)
        # 3. Convert to uppercase
        clean_title = re.sub(r'[^\w\s]', '', title).replace(' ', '_').upper()
        
        # Determine prefix for sorting
        if "PROLOGUE" in clean_title or "DEDICATION" in clean_title or "COPYRIGHT" in clean_title:
            prefix = "00"
        elif "EPILOGUE" in clean_title or "ABOUT_THE_AUTHOR" in clean_title:
            prefix = "99"
        else:
            # All other sub-chapters are numbered sequentially
            prefix = f"{i:02d}"
            
        filename = f"{prefix}_{clean_title}.txt"
        file_path = OUTPUT_DIR / filename
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"  -> Saved: {filename} ({len(content)} chars)")
        
    print("Extraction complete.")

def main():
    if not PDF_FILE.exists():
        print(f"Error: PDF file not found at {PDF_FILE}")
        return

    raw_text = extract_text_from_pdf(PDF_FILE)
    if not raw_text:
        return

    # Save raw text for debugging
    with open(PROJECT_ROOT / "raw_pdf_text.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)
    print(f"Raw PDF text saved to {PROJECT_ROOT / 'raw_pdf_text.txt'}")

    sections = hybrid_chapter_extraction(raw_text)
    
    if sections:
        save_chapters(sections)
    else:
        print("No sections were extracted. Check the PDF content and regex pattern.")

if __name__ == "__main__":
    main()
