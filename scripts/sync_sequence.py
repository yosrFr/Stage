from sqlalchemy import text

from database.session import SessionLocal

TABLES = {
    "category": "category_id",
    "chapter": "chapter_id",
    "control": "control_id",
    "control_tags": "control_tag_id",
    "family_norm": "family_norm_id",
    "language": "language_id",
    "norms": "norm_id"
}

db = SessionLocal()

for table, column in TABLES.items():
    db.execute(text(f"""
                    SELECT setval(
                                   pg_get_serial_sequence('{table}', '{column}'),
                                   COALESCE((SELECT MAX({column}) FROM {table}), 1)
                           )
                    """))

db.commit()
