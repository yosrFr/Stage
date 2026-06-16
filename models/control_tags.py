from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from models.base import Base


class ControlTags(Base):
    __tablename__ = 'control_tags'

    control_tag_id = Column(Integer, primary_key=True)

    control_tag_languages = relationship("ControlTagLanguage", back_populates="control_tag")
    controls = relationship("Control", back_populates="control_tags")
