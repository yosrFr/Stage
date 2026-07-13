from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from scripts.endpointodoo import fetch_active_opportunities, get_existing_opportunity_ids, get_or_create_customer, get_pg_connection
from services.database.import_service import get_or_create_norm
from services.opportunities import get_imported_opportunities_from_db, insert_or_update_audit, sync_cleanup_db, update_protection_needs_in_db


router = APIRouter(prefix="/opportunities", tags=["opportunities"])


@router.get("/")
def get_opportunities():
    result, error, status = fetch_active_opportunities()
    if error:
         raise HTTPException(status_code=status, detail=error)

    existing_ids = get_existing_opportunity_ids()
    result = [o for o in result if o["opportunity_id"] not in existing_ids]

    return result

@router.post("/import/{opportunity_id}")
def import_opportunity(opportunity_id: int):
    all_opportunities, error, status = fetch_active_opportunities()
    if error:
        raise HTTPException(status_code=status, detail=error)

    matching = next((o for o in all_opportunities if o["opportunity_id"] == opportunity_id), None)
    if not matching:
        raise HTTPException(status_code=404, detail="Opportunity not found or not tagged as audit")

    audits = matching["audits"]
    customer_info = matching["customer_information"]
    contact_info = matching["contact_information"]

    conn = get_pg_connection()
    cur = conn.cursor()

    try:
        customer_id = get_or_create_customer(cur, customer_info, contact_info.get("main_contact"))
        norm_id = get_or_create_norm(cur, audits.get("norme"))

        insert_or_update_audit(
            cur, opportunity_id, customer_id, norm_id,
            audits.get("title"), audits.get("type"), audits.get("date_of_order")
        )

        conn.commit()
        return {
            "status": "success",
            "opportunity_id": opportunity_id,
            "customer_id": customer_id,
            "norm_id": norm_id
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

class ProtectionNeedsUpdate(BaseModel):
    protection_needs: str


@router.post("/sync-cleanup")
def sync_cleanup():
    current_opportunities, error, status = fetch_active_opportunities()
    if error:
        raise HTTPException(status_code=status, detail=error)

    active_ids = [o["opportunity_id"] for o in current_opportunities]

    try:
        deleted_audits, deleted_customers = sync_cleanup_db(active_ids)
        return {
            "status": "cleaned",
            "deleted_audits": deleted_audits,
            "deleted_customers": deleted_customers,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/imported-opportunities")
def get_imported_opportunities():
    try:
        return get_imported_opportunities_from_db()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/audit/{opportunity_id}/protection-needs")
def update_protection_needs(opportunity_id: int, payload: ProtectionNeedsUpdate):
    valid_values = ["normal", "high", "very high"]
    if payload.protection_needs not in valid_values:
        raise HTTPException(status_code=400, detail=f"Valeur invalide. Attendu : {valid_values}")

    try:
        update_protection_needs_in_db(opportunity_id, payload.protection_needs)
        return {"status": "updated", "opportunity_id": opportunity_id, "protection_needs": payload.protection_needs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))