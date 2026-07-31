import psycopg2
import requests

PG_CONFIG = {
    "host": "db",
    "port": "5432",
    "dbname": "mydb",
    "user": "postgres",
    "password": "postgres",
}

base_url = "https://audit12.odoo.com/"
api_key = "87b8b77186062dfee49203d13fb07b545a303d9c"
db_name = "audit12"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "X-Odoo-Database": db_name,
}


def get_pg_connection():
    return psycopg2.connect(**PG_CONFIG)


def ensure_column(table_name, column_name, column_type):
    conn = get_pg_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};")
        conn.commit()
        print(f"Colonne '{column_name}' ajoutée à '{table_name}'.")
    except psycopg2.errors.DuplicateColumn:
        conn.rollback()
        print(f"Colonne '{column_name}' déjà existante dans '{table_name}', rien à faire.")
    finally:
        cur.close()
        conn.close()


def fix_sequence(cur, table_name, id_column):
    cur.execute(f"""
        SELECT setval(
            pg_get_serial_sequence('{table_name}', '{id_column}'),
            COALESCE((SELECT MAX({id_column}) FROM {table_name}), 1)
        )
    """)


def fix_all_sequences():
    conn = get_pg_connection()
    cur = conn.cursor()
    try:
        fix_sequence(cur, "language", "language_id")
        fix_sequence(cur, "norms", "norm_id")
        fix_sequence(cur, "customers", "customer_id")
        fix_sequence(cur, "audit", "audit_id")
        conn.commit()
        print("Séquences resynchronisées.")
    except Exception as e:
        conn.rollback()
        print("Erreur lors de la resynchronisation :", e)
    finally:
        cur.close()
        conn.close()


def run_startup_setup():
    ensure_column("audit", "opportunity_id", "INTEGER UNIQUE")
    ensure_column("audit", "protection_needs", "VARCHAR(50)")
    ensure_column("audit", "category_id", "INTEGER")
    fix_all_sequences()

LANGUAGE_MAPPING = {
    "english": "english",
    "english (us)": "english",
    "en_us": "english",
    "en": "english",
    "german": "deutsch",
    "deutsch": "deutsch",
    "german / deutsch": "deutsch",
    "de_de": "deutsch",
    "de": "deutsch",
}


def get_existing_opportunity_ids():
    conn = get_pg_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT opportunity_id FROM audit WHERE opportunity_id IS NOT NULL")
        rows = cur.fetchall()
        return set(r[0] for r in rows)
    finally:
        cur.close()
        conn.close()


def get_or_create_language(cur, language_name):
    if not language_name:
        return None

    key = language_name.strip().lower()
    mapped_name = LANGUAGE_MAPPING.get(key)

    if mapped_name:
        cur.execute("SELECT language_id FROM language WHERE language = %s", (mapped_name,))
        row = cur.fetchone()
        if row:
            return row[0]

    cur.execute("SELECT language_id FROM language WHERE language ILIKE %s", (f"%{language_name}%",))
    row = cur.fetchone()
    if row:
        return row[0]

    return None


def get_default_family_norm_id(cur):
    cur.execute("SELECT family_norm_id FROM family_norm LIMIT 1")
    row = cur.fetchone()
    if row:
        return row[0]
    raise Exception("Aucune ligne dans la table 'family_norm' — il faut en créer au moins une manuellement dans pgAdmin avant d'importer.")


def get_or_create_norm(cur, norm_title):
    if not norm_title:
        norm_title = "N/A"
    cur.execute("SELECT norm_id FROM norms WHERE title = %s", (norm_title,))
    row = cur.fetchone()
    if row:
        return row[0]

    family_norm_id = get_default_family_norm_id(cur)

    cur.execute("""
        INSERT INTO norms (title, abbreviation, publish_year, family_norm_id)
        VALUES (%s, %s, %s, %s)
        RETURNING norm_id
    """, (norm_title, "N/A", 0, family_norm_id))
    return cur.fetchone()[0]


def get_or_create_customer(cur, customer_info, main_contact_name):
    company_name = customer_info.get("company_name") or "N/A"
    street = customer_info.get("street") or "N/A"
    zip_code = customer_info.get("zip") or "N/A"
    location = customer_info.get("location") or "N/A"
    country = customer_info.get("country") or "N/A"
    email = customer_info.get("email") or "N/A"
    phone = customer_info.get("phone") or "N/A"
    main_contact_name = main_contact_name or "N/A"
    account_manager = main_contact_name

    cur.execute("SELECT customer_id FROM customers WHERE name = %s", (company_name,))
    row = cur.fetchone()

    language_id = get_or_create_language(cur, customer_info.get("language"))

    if row:
        customer_id = row[0]
        cur.execute("""
            UPDATE customers SET
                street = %s, zip = %s, location = %s, country = %s,
                email = %s, phone_number = %s, main_contact = %s, language_id = %s,
                account_manager = %s
            WHERE customer_id = %s
        """, (
            street, zip_code, location, country,
            email, phone, main_contact_name, language_id,
            account_manager, customer_id
        ))
        return customer_id
    else:
        cur.execute("""
            INSERT INTO customers (name, street, zip, location, country, email, phone_number, main_contact, language_id, account_manager)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING customer_id
        """, (
            company_name, street, zip_code, location, country,
            email, phone, main_contact_name, language_id, account_manager
        ))
        return cur.fetchone()[0]


def insert_or_update_audit(cur, opportunity_id, customer_id, norm_id, title, audit_type, date_of_order):
    cur.execute("""
        INSERT INTO audit (opportunity_id, customer_id, norm_id, title, type, date_of_order, responsible)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (opportunity_id)
        DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            norm_id = EXCLUDED.norm_id,
            title = EXCLUDED.title,
            type = EXCLUDED.type,
            date_of_order = EXCLUDED.date_of_order
    """, (
        opportunity_id, customer_id, norm_id,
        title or "N/A", audit_type or "N/A", date_of_order, "N/A"
    ))


def get_imported_opportunities_from_db():
    conn = get_pg_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT a.opportunity_id, a.title, n.title AS norm_title, c.name AS customer_name, a.protection_needs
            FROM audit a
            LEFT JOIN norms n ON a.norm_id = n.norm_id
            LEFT JOIN customers c ON a.customer_id = c.customer_id
            WHERE a.opportunity_id IS NOT NULL
            ORDER BY a.audit_id DESC
        """)
        rows = cur.fetchall()

        result = []
        for row in rows:
            opportunity_id, title, norm_title, customer_name, protection_needs = row
            result.append({
                "opportunity_id": opportunity_id,
                "audits": {
                    "title": title,
                    "norme": norm_title,
                    "protection_needs": protection_needs,
                },
                "customer_information": {
                    "company_name": customer_name,
                }
            })
        return result
    finally:
        cur.close()
        conn.close()


def update_protection_needs_in_db(opportunity_id, protection_needs):
    conn = get_pg_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE audit SET protection_needs = %s
            WHERE opportunity_id = %s
        """, (protection_needs, opportunity_id))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def sync_cleanup_db(active_ids):
    conn = get_pg_connection()
    cur = conn.cursor()
    try:
        if active_ids:
            cur.execute("""
                DELETE FROM audit
                WHERE opportunity_id IS NOT NULL
                AND opportunity_id NOT IN %s
            """, (tuple(active_ids),))
        else:
            cur.execute("DELETE FROM audit WHERE opportunity_id IS NOT NULL")

        deleted_audits = cur.rowcount

        cur.execute("""
            DELETE FROM customers
            WHERE customer_id NOT IN (
                SELECT DISTINCT customer_id FROM audit WHERE customer_id IS NOT NULL
            )
        """)
        deleted_customers = cur.rowcount

        conn.commit()
        return deleted_audits, deleted_customers
    finally:
        cur.close()
        conn.close()




def fetch_active_opportunities():
    endpoint = f"{base_url}/json/2/crm.lead/search_read"

    payload = {
        "domain": [["stage_id.name", "=", "Project Execution Start"]],
        "fields": [
            "id", "name", "partner_id", "contact_name", "email_from", "phone",
            "street", "zip", "city", "country_id", "lang_id",
            "x_studio_product", "x_studio_date_of_order", "stage_id"
        ]
    }

    resp = requests.post(endpoint, headers=headers, json=payload)

    if resp.status_code != 200:
        return None, resp.json(), resp.status_code

    opportunities = resp.json()
    result = []

    for opp in opportunities:
        opportunity_id = opp.get("id")
        partner_field = opp.get("partner_id")
        product_field = opp.get("x_studio_product")
        country_field = opp.get("country_id")
        lang_field = opp.get("lang_id")
        contact_name = opp.get("contact_name")

        company_name = partner_field[1] if partner_field else None
        partner_id = partner_field[0] if partner_field else None

        norme = product_field[1] if product_field else None
        product_id = product_field[0] if product_field else None

        audit_type = "internal audit"
        date_order = opp.get("x_studio_date_of_order")
        language = lang_field[1] if lang_field else None

        product_tag_name = None
        product_tag_id = None
        if product_id:
            tag_endpoint = f"{base_url}/json/2/product.template/search_read"
            tag_payload = {
                "domain": [["id", "=", product_id]],
                "fields": ["x_studio_product_tag"]
            }
            tag_resp = requests.post(tag_endpoint, headers=headers, json=tag_payload)
            if tag_resp.status_code == 200:
                tag_data = tag_resp.json()
                if tag_data:
                    tag_field = tag_data[0].get("x_studio_product_tag")
                    if tag_field:
                        product_tag_id = tag_field[0]
                        product_tag_name = tag_field[1]
        if not product_tag_name or product_tag_name.lower() != "audit":
            continue

        contact_email = None
        contact_phone = None
        contact_id = None

        if contact_name:
            contact_endpoint = f"{base_url}/json/2/res.partner/search_read"
            contact_payload = {
                "domain": [["name", "ilike", contact_name]],
                "fields": ["id", "name", "email", "phone"],
                "limit": 1
            }
            contact_resp = requests.post(contact_endpoint, headers=headers, json=contact_payload)
            if contact_resp.status_code == 200:
                contact_data = contact_resp.json()
                if contact_data:
                    contact_id = contact_data[0].get("id")
                    contact_email = contact_data[0].get("email")
                    contact_phone = contact_data[0].get("phone")

        title = f"{date_order} - {company_name} - {audit_type}"

        audits = {
            "id": opportunity_id,
            "norme": norme,
            "product_id": product_id,
            "product_tag": product_tag_name,
            "product_tag_id": product_tag_id,
            "type": audit_type,
            "date_of_order": date_order,
            "title": title,
        }

        customer_info = {
            "id": partner_id,
            "company_name": company_name,
            "street": opp.get("street"),
            "zip": opp.get("zip"),
            "location": opp.get("city"),
            "country": country_field[1] if country_field else None,
            "language": language,
            "email": opp.get("email_from"),
            "phone": opp.get("phone"),
        }

        contact_info = {
            "id": contact_id,
            "main_contact": contact_name,
            "email": contact_email,
            "phone": contact_phone,
        }

        internal_account_manager = {
            "name": contact_name,
            "email": contact_email,
            "notes": None,
        }

        result.append({
            "opportunity_id": opportunity_id,
            "audits": audits,
            "customer_information": customer_info,
            "contact_information": contact_info,
            "internal_account_manager": internal_account_manager,
        })

    return result, None, 200