"""
Game Completion Date Normalizer
-------------------------------

Purpose:
Convert Obsidian game tracker frontmatter dates from HowLongToBeat's
MM/DD/YY format to ISO YYYY-MM-DD format so Obsidian Bases can
recognize the field as a true Date and sort correctly.

Example:
    Completion Date: "6/18/26"
becomes:
    Completion Date: "2026-06-18"

Features:
- Processes all .md files in the specified folder.
- Converts only the 'Completion Date' field.
- Leaves files without a completion date unchanged.
- Supports both quoted and unquoted dates.
- Interprets two-digit years as:
      00–30 -> 2000–2030
      31–99 -> 1931–1999
- Writes changes directly to the files.

Recommended workflow:
1. Back up the folder before running.
2. Run the script.
3. Change the Obsidian Base field type from Text to Date.
4. Verify sorting and filtering work correctly.

Created for an Obsidian game library imported from
HowLongToBeat exports.
"""

from pathlib import Path
import re
from datetime import datetime

# Change this to your actual Obsidian games folder
FOLDER = Path("/Users/cgoodwin/Databases/TheVault/6.0 - Personal/Video Games")

date_re = re.compile(r'^(Completion Date:\s*)"?(\d{1,2}/\d{1,2}/\d{2,4})"?\s*$', re.MULTILINE)

def convert_date(date_text):
    month, day, year = date_text.split("/")
    year = int(year)

    if year < 100:
        # Treat 00–30 as 2000–2030; 31–99 as 1931–1999
        year = 2000 + year if year <= 30 else 1900 + year

    return f"{year:04d}-{int(month):02d}-{int(day):02d}"

for path in FOLDER.glob("*.md"):
    text = path.read_text(encoding="utf-8")

    def replace(match):
        prefix = match.group(1)
        old_date = match.group(2)
        new_date = convert_date(old_date)
        return f'{prefix}"{new_date}"'

    new_text = date_re.sub(replace, text)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"Updated: {path.name}")

print("Done.")