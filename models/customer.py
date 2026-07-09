from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class Customer(Base):
    """
    Customer Table - Organizations being audited
    PRIMARY KEY: customer_id
    """
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    street = Column(String(200), nullable=False)
    zip = Column(String(20), nullable=False)
    location = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    account_manager = Column(String(200), nullable=False)
    manager_email = Column(String(100))
    main_contact = Column(String(200), nullable=False)
    manager_notes = Column(String(1000))
    language_id = Column(Integer, ForeignKey("language.language_id"), nullable=False)

    # RELATIONSHIPS
    # One-to-Many: Customer -> Audit
    # A customer can have multiple audits
    audits = relationship("Audit", back_populates="customer", cascade="all, delete-orphan")
    # A customer have language, and a language can be used by multiple customers
    language = relationship("Language", back_populates="customers")