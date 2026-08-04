from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from models.base import Base


class ReportConfig(Base):
    __tablename__ = "report_config"

    report_config_id = Column(Integer, primary_key=True, autoincrement=True)
    family_norm_id = Column(Integer, nullable=False, unique=True)

    background = Column(Text)
    cover_page_logo = Column(Text)
    header_logo = Column(Text)
    last_page_background = Column(Text)

    web_page_link = Column(String(500))

    evaluation_results_summary = Column(Boolean, default=True)
    risk_level_dist = Column(Boolean, default=True)
    maturity_level_assessment = Column(Boolean, default=True)
    list_non_conformity = Column(Boolean, default=True)

    initiation = Column(Text)
    introduction = Column(Text)
    organisation = Column(Text)

    overall_summary_chart_title = Column(String(300))
    maturity_assessment_section_title = Column(String(300))
    maturity_assessment_chart_title = Column(String(300))

    report_title_font_family = Column(String(100))
    report_title_font_color = Column(String(20))
    report_title_font_size = Column(Integer)

    header1_font_family = Column(String(100))
    header1_font_color = Column(String(20))
    header1_font_size = Column(Integer)

    header2_font_family = Column(String(100))
    header2_font_color = Column(String(20))
    header2_font_size = Column(Integer)

    header3_font_family = Column(String(100))
    header3_font_color = Column(String(20))
    header3_font_size = Column(Integer)

    text_font_family = Column(String(100))
    text_font_color = Column(String(20))
    text_font_size = Column(Integer)

    table_header_bg_color = Column(String(20))
    audit_report_color_1 = Column(String(20))
    audit_report_color_2 = Column(String(20))
    gradient = Column(Boolean, default=True)

    list_abbreviation = Column(JSONB, default=list)
    maturity_levels = Column(JSONB, default=list)
    risk_levels = Column(JSONB, default=list)