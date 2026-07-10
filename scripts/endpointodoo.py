from flask import Flask, jsonify
from flask_cors import CORS
import requests
import psycopg2

app = Flask(__name__)
CORS(app)

base_url = "https://e-n-s.odoo.com/"
api_key = " 240f8f421eaa1d0131ad8d64fe8bc198edf2c82c"
db_name = "e-n-s"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "X-Odoo-Database": db_name,
}

PG_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "auditaas",
    "user": "postgres",
    "password": "admin",
    
}


def get_pg_connection():
    return psycopg2.connect(**PG_CONFIG)


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


def fetch_active_opportunities():
    """
    Récupère les opportunités actives depuis Odoo (taguées 'audit', stage 'Project Execution Start').
    Ne filtre PAS par ce qui est déjà importé en base — c'est la source de vérité brute,
    utilisée par /opportunities (qui filtre ensuite), /import et /sync-cleanup.
    """
    endpoint = f"{base_url}/json/2/crm.lead/search_read"

    payload = {
        "domain": [["stage_id.name", "=", "Project Execution Start"]],
        "fields": [
            "id", "name", "partner_id", "contact_name", "email_from", "phone",
            "street", "zip", "city", "country_id", "lang_id",
            "x_studio_product", "x_studio_date", "stage_id"
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
        date_order = opp.get("x_studio_date")
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
                "domain": [
                    ["name", "ilike", contact_name]
                ],
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


@app.route("/opportunities", methods=["GET"])
def get_opportunities():
    result, error, status = fetch_active_opportunities()
    if error:
        return jsonify({"error": error}), status

    existing_ids = get_existing_opportunity_ids()
    result = [o for o in result if o["opportunity_id"] not in existing_ids]

    return jsonify(result)


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


@app.route("/import/<int:opportunity_id>", methods=["POST"])
def import_opportunity(opportunity_id):
    all_opportunities, error, status = fetch_active_opportunities()
    if error:
        return jsonify({"error": error}), status

    matching = next((o for o in all_opportunities if o["opportunity_id"] == opportunity_id), None)
    if not matching:
        return jsonify({"error": "Opportunity not found or not tagged as audit"}), 404

    audits = matching["audits"]
    customer_info = matching["customer_information"]
    contact_info = matching["contact_information"]

    conn = get_pg_connection()
    cur = conn.cursor()

    try:
        customer_id = get_or_create_customer(cur, customer_info, contact_info.get("main_contact"))
        norm_id = get_or_create_norm(cur, audits.get("norme"))

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
            audits.get("title") or "N/A",
            audits.get("type") or "N/A",
            audits.get("date_of_order"),
            "N/A"
        ))

        conn.commit()
        return jsonify({
            "status": "success",
            "opportunity_id": opportunity_id,
            "customer_id": customer_id,
            "norm_id": norm_id
        })

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
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


def ensure_opportunity_id_column():
    conn = get_pg_connection()
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE audit ADD COLUMN opportunity_id INTEGER UNIQUE;")
        conn.commit()
        print("Colonne 'opportunity_id' ajoutée.")
    except psycopg2.errors.DuplicateColumn:
        conn.rollback()
        print("Colonne 'opportunity_id' déjà existante, rien à faire.")
    finally:
        cur.close()
        conn.close()


ensure_opportunity_id_column()
fix_all_sequences()


@app.route("/sync-cleanup", methods=["POST"])
def sync_cleanup():
    current_opportunities, error, status = fetch_active_opportunities()
    if error:
        return jsonify({"error": error}), status

    active_ids = [o["opportunity_id"] for o in current_opportunities]

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
        return jsonify({
            "status": "cleaned",
            "deleted_audits": deleted_audits,
            "deleted_customers": deleted_customers,
        })
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)