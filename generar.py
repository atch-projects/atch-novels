
import os
import json
import re


# =========================
# CONFIGURATION
# =========================

NOVELS_FOLDER = "novelas"


# =========================
# NATURAL SORT
# =========================

def natural_sort(value):
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", value)
    ]


# =========================
# READ NOVELS
# =========================

novels = []

for novel in sorted(os.listdir(NOVELS_FOLDER), key=natural_sort):

    novel_path = os.path.join(NOVELS_FOLDER, novel)

    if not os.path.isdir(novel_path):
        continue

    chapters = []

    # Read chapters
    for file in sorted(os.listdir(novel_path), key=natural_sort):

        if file.lower().endswith(".txt"):

            file_path = os.path.join(novel_path, file)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            chapters.append({
                "name": os.path.splitext(file)[0],
                "content": content
            })

    novels.append({
        "name": novel,
        "chapters": chapters
    })


# =========================
# GENERATE JSON
# =========================

with open("novelas.json", "w", encoding="utf-8") as f:
    json.dump(novels, f, ensure_ascii=False, indent=4)


print("JSON generated successfully!")
