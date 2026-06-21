"""
Book Date Read Normalizer
-------------------------

Purpose:
Convert Obsidian book tracker frontmatter dates from Goodreads-style
MM/DD/YY format to ISO YYYY-MM-DD format so Obsidian Bases can
recognize the field as a true Date and sort correctly.

Example:
    Date Read: "10/26/23"
becomes:
    Date Read: "2023-10-26"

Features:
- Processes all .md files in the specified folder.
- Converts only the 'Date Read' field.
- Preserves blank dates:
      Date Read:
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

Created for an Obsidian reading tracker imported from
Goodreads export data.
"""

from pathlib import Path
import re

# Change this to your actual Obsidian books folder
FOLDER = Path("/Users/cgoodwin/Databases/TheVault/6.0 - Personal/Reading/Fiction Books Read")

date_re = re.compile(
    r'^(Date Read:\s*)"?(\d{1,2}/\d{1,2}/\d{2,4})"?\s*$',
    re.MULTILINE
)

def convert_date(date_text):
    month, day, year = date_text.split("/")
    year = int(year)

    if year < 100:
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