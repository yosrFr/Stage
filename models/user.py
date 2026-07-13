from datetime import datetime
from sqlalchemy import ARRAY, Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    """
    User Table - System users and auditors
    PRIMARY KEY: user_id
    """
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    firstname = Column(String(50))
    lastname = Column(String(50))
    # fields for Keycloak integration
    keycloak_id = Column(String(255), unique=True, nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    roles = Column(ARRAY(String), default=list, nullable=True)
    groups = Column(ARRAY(String), default=list, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # RELATIONSHIPS
    # One-to-Many: One user can manage multiple audits as the main contact
    managed_audits = relationship(
    "Audit",
    back_populates="main_contact",
    foreign_keys="Audit.main_contact_id"
    )

    # One-to-Many: One user can approve multiple audits
    approved_audits = relationship(
    "Audit",
    back_populates="lead_auditor",
    foreign_keys="Audit.lead_auditor_id"
    )
    # One-to-Many: User -> AuditActivity (as auditor)
    # A user can participate in multiple audit activities (audit_activities)
    # audit_activities = relationship("AuditActivity", back_populates="auditor")
    # Many-to-Many: User <-> Audit via UserAudit
    # user_audits = relationship("UserAudit", back_populates="user")
def __repr__(self):
    return f"<User(username='{self.username}', email='{self.email}')>"
