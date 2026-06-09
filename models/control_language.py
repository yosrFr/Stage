from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base import Base


class ControlLanguage(Base):
    __tablename__ = 'control_language'

    control_id = Column(Integer, ForeignKey("control.control_id"), primary_key=True)
    language_id = Column(Integer, ForeignKey("language.language_id"), primary_key=True)
    title = Column(Text, nullable=False)
    description = Column(Text)

    control = relationship("Control", back_populates="control_languages")
    languages = relationship("Language", back_populates="control_languages")