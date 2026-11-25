
import os
import json
import re


# =========================
# CONFIGURATION
# =========================

NOVELS_FOLDER = "novels"
CHAPTERS_FOLDER = "chapters"
OUTPUT_FILE = "database.json"

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")


# =========================
# NATURAL SORT
# =========================

def natural_sort(value):
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", value)
    ]


# =========================
# CREATE MAIN FOLDER
# =========================

os.makedirs(NOVELS_FOLDER, exist_ok=True)


# =========================
# READ NOVELS
# =========================

novels = []

for novel in sorted(os.listdir(NOVELS_FOLDER), key=natural_sort):

    novel_path = os.path.join(NOVELS_FOLDER, novel)

    if not os.path.isdir(novel_path):
        continue

    # =========================
    # CREATE CHAPTERS FOLDER
    # =========================

    chapters_path = os.path.join(novel_path, CHAPTERS_FOLDER)

    os.makedirs(chapters_path, exist_ok=True)

    # =========================
    # FIND COVER IMAGE
    # =========================

    image = None

    for file in sorted(os.listdir(novel_path), key=natural_sort):

        if file.lower().endswith(IMAGE_EXTENSIONS):

            image = file
            break

    # =========================
    # READ CHAPTERS
    # =========================

    chapters = []

    for file in sorted(os.listdir(chapters_path), key=natural_sort):

        if file.lower().endswith(".txt"):

            file_path = os.path.join(chapters_path, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            chapters.append({
                "name": os.path.splitext(file)[0],
                "content": content
            })

    # =========================
    # ADD NOVEL
    # =========================

    novels.append({
        "name": novel,
        "image": image,
        "chapters": chapters
    })


# =========================
# GENERATE JSON
# =========================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(
        novels,
        f,
        ensure_ascii=False,
        indent=4
    )


# =========================
# SUMMARY
# =========================

print("JSON generated successfully!")
print(f"Total novels: {len(novels)}")

for novel in novels:
    print(f"- {novel['name']}: {len(novel['chapters'])} chapters")

print(f"\nOutput file: {OUTPUT_FILE}")
