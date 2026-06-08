from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Chapter(Base):
    __tablename__ ='chapter'

    chapter_id = Column(Integer, primary_key=True)
    id = Column(String(200), nullable=False)
    norm_id = Column(Integer, ForeignKey('norms.norm_id'), nullable=False)

    norm = relationship("Norm", back_populates="chapters")
    controls = relationship("Control", back_populates="chapter")
    chapter_languages = relationship("ChapterLanguage", back_populates="chapter")