import re
from pathlib import Path

PROJECT_ROOT = Path("/home/ubuntu/audiobooksmith_project")
RAW_TEXT_FILE = PROJECT_ROOT / "raw_pdf_text.txt"

def analyze_titles():
    if not RAW_TEXT_FILE.exists():
        print(f"Error: Raw text file not found at {RAW_TEXT_FILE}")
        return

    with open(RAW_TEXT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Regex to find lines that are likely titles:
    # 1. Starts with optional whitespace (for centering)
    # 2. Followed by a sequence of words (at least two words)
    # 3. Ends with optional whitespace
    # 4. Must be on its own line (MULTILINE flag)
    
    # Let's look for lines that are mostly capitalized and short (heuristic for titles)
    # We will use a broad pattern and then manually filter the output.
    
    # Pattern: A line that starts with whitespace, contains 2-8 words, and ends with whitespace.
    # This is a very rough heuristic, but should capture the centered titles.
    # The actual titles are: "Once Upon a Time", "My First Misadventure", etc.
    
    # Let's try to capture lines that are not too long and contain at least one capital letter.
    # The raw text shows titles are often centered with many spaces.
    
    # Pattern to capture centered, title-like lines:
    # ^\s* - Start of line, optional whitespace
    # ([\w\s]{5,50}) - Capture group: 5 to 50 characters (words and spaces)
    # \s*$ - Optional whitespace, end of line
    
    pattern = re.compile(r"^\s*([\w\s]{5,50})\s*$", re.MULTILINE)
    
    potential_titles = set()
    
    for match in pattern.finditer(raw_text):
        title = match.group(1).strip()
        
        # Filter out lines that are too short or look like page numbers/junk
        if len(title) > 5 and not re.match(r"^\d+$", title) and not re.match(r"^\w$", title):
            # Check if it's mostly title case or all caps
            if title.istitle() or title.isupper():
                potential_titles.add(title)

    # Manually add the known special pages that might not fit the heuristic
    potential_titles.add("Copyright")
    potential_titles.add("DEDICATION")
    potential_titles.add("CREDITS")
    potential_titles.add("Prologue")
    potential_titles.add("Epilogue")
    potential_titles.add("ABOUT THE AUTHOR")
    potential_titles.add("The Beginning")
    potential_titles.add("Foster Care")
    potential_titles.add("Into Adulthood")
    
    print("--- Potential Chapter Titles ---")
    for title in sorted(list(potential_titles)):
        print(title)

if __name__ == "__main__":
    analyze_titles()
