from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Control(Base):
    __tablename__ = "control"

    control_id = Column(Integer, primary_key=True)
    id = Column(String(200), nullable=False)
    norm_id = Column(Integer, ForeignKey("norms.norm_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    control_tag_id = Column(Integer, ForeignKey("control_tags.control_tag_id"))
    chapter_id = Column(Integer, ForeignKey("chapter.chapter_id"), nullable=False)

    chapter = relationship("Chapter", back_populates="controls")
    categories = relationship("Category", back_populates="controls")
    control_tags = relationship("ControlTags", back_populates="controls")
    norms = relationship("Norm", back_populates="controls")
    control_languages = relationship("ControlLanguage", back_populates="control")