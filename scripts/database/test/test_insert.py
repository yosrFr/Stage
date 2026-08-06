from database.session import SessionLocal
from crud.category_crud import create_category
from crud.category_language_crud import create_category_language
from crud.chapter_crud import create_chapter
from crud.chapter_language_crud import create_chapter_language
from crud.control_crud import create_control
from crud.control_language_crud import create_control_language
from crud.control_tag_language_crud import create_control_tag_language
from crud.control_tags_crud import create_control_tag
from crud.family_norm_crud import create_family_norm
from crud.language_crud import create_language
from crud.norm_crud import create_norm

db = SessionLocal()

create_family_norm(db, {
    "name": "TISAX"
})

create_norm(db, {
    "title": "TISAX ISA v6",
    "abbreviation": "Information Security Directive 2",
    "description": "Information Security at the Organization: Covers organizational responsibilities, policies, and continuous improvement for managing information security.",
    "publish_year": 2025,
    "family_norm_id": 1
})

create_chapter(db, {
    "id": "1.1",
    "norm_id": 1
})

create_control_tag(db, {
})

create_category(db, {
    "id": "1.1",
    "norm_id": 1
})

create_control(db, {
    "id": "1.1",
    "norm_id": 1,
    "category_id": 1,
    "control_tag_id": 1,
    "chapter_id": 1
})

create_language(db, {
    "language": "english"
})

create_control_tag_language(db, {
    "control_tag_id": 1,
    "language_id": 1,
    "title": ""
})

create_chapter_language(db, {
    "chapter_id": 1,
    "language_id": 1,
    "title": "Information Security Policies",
    "objective": ""
})

create_category_language(db, {
    "category_id": 1,
    "language_id": 1,
    "category_name": "english",
})

create_control_language(db, {
    "control_id": 1,
    "language_id": 1,
    "title": "",
    "description": ""
})

db.close()

print("Database populated")
