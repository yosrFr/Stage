from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from models.base import Base


class ChapterLanguage(Base):
    __tablename__ = 'chapter_language'

    chapter_id = Column(Integer, ForeignKey("chapter.chapter_id"), primary_key=True)
    language_id = Column(Integer, ForeignKey("language.language_id"), primary_key=True)
    title = Column(String(500), nullable=False)
    objective = Column(Text)

    chapter = relationship("Chapter", back_populates="chapter_languages")
    languages = relationship("Language", back_populates="chapter_languages")
