from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models.base import Base


class ControlTagLanguage(Base):
    __tablename__ = 'control_tag_language'

    control_tag_id = Column(Integer, ForeignKey('control_tags.control_tag_id'), primary_key=True)
    language_id = Column(Integer, ForeignKey('language.language_id'), primary_key=True)
    title = Column(String(100), unique=True, nullable=False)

    control_tag = relationship("ControlTags", back_populates="control_tag_languages")
    languages = relationship("Language", back_populates="control_tag_languages")
