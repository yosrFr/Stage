import json

from crud.category_crud import create_many_categories
from crud.category_language_crud import create_many_category_languages
from crud.chapter_crud import create_many_chapters
from crud.chapter_language_crud import create_many_chapter_languages
from crud.control_crud import create_many_controls
from crud.control_language_crud import create_many_control_languages
from crud.control_tag_language_crud import create_many_control_tag_languages
from crud.control_tags_crud import create_many_control_tags
from crud.family_norm_crud import create_many_family_norms
from crud.norm_crud import create_many_norms
from crud.language_crud import create_many_languages
from database.session import SessionLocal

db = SessionLocal()


# Populate the table family_norm
with open("../data/family_norm.json", "r", encoding="utf-8") as f:
    family_norms = json.load(f)

create_many_family_norms(db, family_norms)


# Populate the table norm
with open("../data/norms.json", "r", encoding="utf-8") as f:
    norms = json.load(f)

create_many_norms(db, norms)


# Populate the table chapter
with open("../data/chapters.json", "r", encoding="utf-8") as f:
    chapters = json.load(f)

create_many_chapters(db, chapters)


# Populate the table control_tags
with open("../data/control_tags.json", "r", encoding="utf-8") as f:
    control_tags = json.load(f)

create_many_control_tags(db, control_tags)


# Populate the table category
with open("../data/categories.json", "r", encoding="utf-8") as f:
    categories = json.load(f)

create_many_categories(db, categories)


# Populate the table control
with open("../data/controls.json", "r", encoding="utf-8") as f:
    controls = json.load(f)

create_many_controls(db, controls)


# Populate the table language
with open("../data/languages.json", "r", encoding="utf-8") as f:
    languages = json.load(f)

create_many_languages(db, languages)


# Populate the table control_tag_language
with open("../data/control_tag_language.json", "r", encoding="utf-8") as f:
    control_tag_languages = json.load(f)

create_many_control_tag_languages(db, control_tag_languages)


# Populate the table chapter_language
with open("../data/chapter_languages.json", "r", encoding="utf-8") as f:
    chapter_languages = json.load(f)

create_many_chapter_languages(db, chapter_languages)


# Populate the table category_language
with open("../data/category_languages.json", "r", encoding="utf-8") as f:
    category_languages = json.load(f)

create_many_category_languages(db, category_languages)


# Populate the table control_language
with open("../data/control_languages.json", "r", encoding="utf-8") as f:
    control_languages = json.load(f)

create_many_control_languages(db, control_languages)


db.close()
