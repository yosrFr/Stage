import json
from sqlalchemy import text
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
from crud.customer_crud import create_many_customers
from crud.user_crud import create_many_users
from crud.audit_crud import create_many_audits
from crud.language_crud import create_many_languages
from crud.measure_crud import create_many_measures
from crud.finding_crud import create_many_findings
from crud.questionResponse_crud import create_many_question_responses
from crud.responseFinding_crud import create_many_response_findings
from database.session import SessionLocal


db = SessionLocal()
# Liste de toutes les tables à vider avant de reseeder (ordre peu important avec CASCADE)
tables_to_truncate = [
    "audit",
    "control_tags",
    "control_tag_language",
    "control_language",
    "control",
    "chapter_language",
    "chapter",
    "category_language",
    "category",
    "family_norm",
    "users",
    "customers",
    "norms",
    "language",
    "findings",
    "measure",
    "question_responses",
    "response_findings",
]

db.execute(text(f"TRUNCATE TABLE {', '.join(tables_to_truncate)} RESTART IDENTITY CASCADE;"))
db.commit()
print(" Tables truncated, ready to reseed")



# Populate the table family_norm
with open("../data/TISAX/family_norm.json", "r", encoding="utf-8") as f:
    family_norms = json.load(f)

create_many_family_norms(db, family_norms)

# Populate the table norm
with open("../data/TISAX/norms.json", "r", encoding="utf-8") as f:
    norms = json.load(f)

create_many_norms(db, norms)
# Populate the table language
with open("../data/TISAX/languages.json", "r", encoding="utf-8") as f:
    languages = json.load(f)

create_many_languages(db, languages)

# Populate the table customer
with open("../data/customer.json", "r", encoding="utf-8") as f:
    customers = json.load(f)

create_many_customers(db, customers)

# Populate the table user
with open("../data/user.json", "r", encoding="utf-8") as f:
    users = json.load(f)

create_many_users(db, users)

# Populate the table audit
with open("../data/audit.json", "r", encoding="utf-8") as f:
    audits = json.load(f)

create_many_audits(db, audits)


# Populate the table chapter
with open("../data/TISAX/chapters.json", "r", encoding="utf-8") as f:
    chapters = json.load(f)

create_many_chapters(db, chapters)

# Populate the table control_tags
with open("../data/TISAX/control_tags.json", "r", encoding="utf-8") as f:
    control_tags = json.load(f)

create_many_control_tags(db, control_tags)

# Populate the table category
with open("../data/TISAX/categories.json", "r", encoding="utf-8") as f:
    categories = json.load(f)

create_many_categories(db, categories)

# Populate the table control
with open("../data/TISAX/controls.json", "r", encoding="utf-8") as f:
    controls = json.load(f)

create_many_controls(db, controls)

# Populate the table control_tag_language
with open("../data/TISAX/control_tag_language.json", "r", encoding="utf-8") as f:
    control_tag_languages = json.load(f)

create_many_control_tag_languages(db, control_tag_languages)

# Populate the table chapter_language
with open("../data/TISAX/chapter_languages.json", "r", encoding="utf-8") as f:
    chapter_languages = json.load(f)

create_many_chapter_languages(db, chapter_languages)

# Populate the table category_language
with open("../data/TISAX/category_languages.json", "r", encoding="utf-8") as f:
    category_languages = json.load(f)

create_many_category_languages(db, category_languages)

# Populate the table control_language
with open("../data/TISAX/control_languages.json", "r", encoding="utf-8") as f:
    control_languages = json.load(f)

create_many_control_languages(db, control_languages)

# Populate the table question_response
with open("../data/TISAX/questionResponses.json", "r", encoding="utf-8") as f:
    question_responses = json.load(f)

create_many_question_responses(db, question_responses)

# Populate the table measure
with open("../data/TISAX/measures.json", "r", encoding="utf-8") as f:
    measures = json.load(f)

create_many_measures(db, measures)

# Populate the table finding
with open("../data/TISAX/findings.json", "r", encoding="utf-8") as f:
    findings = json.load(f)

create_many_findings(db, findings)

# Populate the table response_finding
with open("../data/TISAX/responseFindings.json", "r", encoding="utf-8") as f:
    response_findings = json.load(f)

create_many_response_findings(db, response_findings)

db.close()
