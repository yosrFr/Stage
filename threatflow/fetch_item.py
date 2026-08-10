import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5432"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def fetch_item_by_id(item_id: int):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

            cur.execute(
                """
                SELECT id AS item_id,
                       category,
                       title,
                       summary,
                       severity,
                       cvss_score,
                       cvss_vector,
                       cvss_version
                FROM items
                WHERE id = %s
                """,
                (item_id,),
            )
            item = cur.fetchone()
            if item is None:
                return None
            item = dict(item)

            cur.execute(
                "SELECT actor FROM item_actors WHERE item_id = %s",
                (item_id,),
            )
            item["actors"] = [row["actor"] for row in cur.fetchall()]

            cur.execute(
                "SELECT family FROM item_malware_families WHERE item_id = %s",
                (item_id,),
            )
            item["families"] = [row["family"] for row in cur.fetchall()]

            cur.execute(
                "SELECT ioc_type, ioc_value FROM item_iocs WHERE item_id = %s",
                (item_id,),
            )
            iocs = [{"type": row["ioc_type"], "value": row["ioc_value"]} for row in cur.fetchall()]
            item["iocs"] = iocs
            item["iocs_total"] = len(iocs)

            cur.execute(
                """
                SELECT steps
                FROM item_playbooks
                WHERE item_id = %s
                ORDER BY computed_at DESC LIMIT 1
                """,
                (item_id,),
            )
            playbook_row = cur.fetchone()
            item["playbook_steps"] = playbook_row["steps"] if playbook_row else []

            return item

    finally:
        conn.close()
