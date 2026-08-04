from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.engine import get_db
from services.opportunities import get_pg_connection
from crud.report_config_crud import (
    get_report_config,
    get_or_create_report_config,
    update_report_config,
    update_report_image,
)

router = APIRouter(prefix="/report-config", tags=["report-config"])


class AbbreviationRow(BaseModel):
    abbreviation: str = ""
    description: str = ""


class LevelRow(BaseModel):
    name: str = ""
    color: str = "#000000"
    description: str = ""


class ReportConfigUpdate(BaseModel):
    web_page_link: str | None = None
    evaluation_results_summary: bool | None = None
    risk_level_dist: bool | None = None
    maturity_level_assessment: bool | None = None
    list_non_conformity: bool | None = None
    initiation: str | None = None
    introduction: str | None = None
    organisation: str | None = None
    overall_summary_chart_title: str | None = None
    maturity_assessment_section_title: str | None = None
    maturity_assessment_chart_title: str | None = None
    report_title_font_family: str | None = None
    report_title_font_color: str | None = None
    report_title_font_size: int | None = None
    header1_font_family: str | None = None
    header1_font_color: str | None = None
    header1_font_size: int | None = None
    header2_font_family: str | None = None
    header2_font_color: str | None = None
    header2_font_size: int | None = None
    header3_font_family: str | None = None
    header3_font_color: str | None = None
    header3_font_size: int | None = None
    text_font_family: str | None = None
    text_font_color: str | None = None
    text_font_size: int | None = None
    table_header_bg_color: str | None = None
    audit_report_color_1: str | None = None
    audit_report_color_2: str | None = None
    gradient: bool | None = None
    list_abbreviation: list[AbbreviationRow] | None = None
    maturity_levels: list[LevelRow] | None = None
    risk_levels: list[LevelRow] | None = None


class ImageUpload(BaseModel):
    image_base64: str


def serialize_config(config) -> dict:
    return {
        "family_norm_id": config.family_norm_id,
        "background": config.background,
        "cover_page_logo": config.cover_page_logo,
        "header_logo": config.header_logo,
        "last_page_background": config.last_page_background,
        "web_page_link": config.web_page_link,
        "evaluation_results_summary": config.evaluation_results_summary,
        "risk_level_dist": config.risk_level_dist,
        "maturity_level_assessment": config.maturity_level_assessment,
        "list_non_conformity": config.list_non_conformity,
        "initiation": config.initiation,
        "introduction": config.introduction,
        "organisation": config.organisation,
        "overall_summary_chart_title": config.overall_summary_chart_title,
        "maturity_assessment_section_title": config.maturity_assessment_section_title,
        "maturity_assessment_chart_title": config.maturity_assessment_chart_title,
        "report_title": {
            "font_family": config.report_title_font_family,
            "font_color": config.report_title_font_color,
            "font_size": config.report_title_font_size,
        },
        "header1": {
            "font_family": config.header1_font_family,
            "font_color": config.header1_font_color,
            "font_size": config.header1_font_size,
        },
        "header2": {
            "font_family": config.header2_font_family,
            "font_color": config.header2_font_color,
            "font_size": config.header2_font_size,
        },
        "header3": {
            "font_family": config.header3_font_family,
            "font_color": config.header3_font_color,
            "font_size": config.header3_font_size,
        },
        "text": {
            "font_family": config.text_font_family,
            "font_color": config.text_font_color,
            "font_size": config.text_font_size,
        },
        "table_header_bg_color": config.table_header_bg_color,
        "audit_report_colors": {
            "color_1": config.audit_report_color_1,
            "color_2": config.audit_report_color_2,
        },
        "gradient": config.gradient,
        "list_abbreviation": config.list_abbreviation or [],
        "maturity_levels": config.maturity_levels or [],
        "risk_levels": config.risk_levels or [],
    }


@router.get("/family-norms")
def list_family_norms():
    conn = get_pg_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT family_norm_id, name FROM family_norm ORDER BY name")
        rows = cur.fetchall()
        return [{"family_norm_id": r[0], "name": r[1]} for r in rows]
    finally:
        cur.close()
        conn.close()


@router.get("/{family_norm_id}")
def get_report_config_route(family_norm_id: int, db: Session = Depends(get_db)):
    config = get_report_config(db, family_norm_id)
    if not config:
        return {"exists": False}
    result = serialize_config(config)
    result["exists"] = True
    return result


@router.patch("/{family_norm_id}")
def patch_report_config(family_norm_id: int, payload: ReportConfigUpdate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_unset=True)
    update_report_config(db, family_norm_id, data)
    config = get_or_create_report_config(db, family_norm_id)
    return serialize_config(config)


@router.post("/{family_norm_id}/image/{field_name}")
def upload_report_image(family_norm_id: int, field_name: str, payload: ImageUpload, db: Session = Depends(get_db)):
    valid_fields = ["background", "cover_page_logo", "header_logo", "last_page_background"]
    if field_name not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Champ invalide. Attendu : {valid_fields}")

    update_report_image(db, family_norm_id, field_name, payload.image_base64)
    return {"status": "updated", "field": field_name}