from sqlalchemy import VARCHAR, Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base import Base


class Audit(Base):
    __tablename__ = "audit"

    # -------------------------
    # Columns
    # -------------------------
    
    audit_id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, unique=True, nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    norm_id = Column(Integer, ForeignKey("norms.norm_id"), nullable=False)
    responsible = Column(String(100), nullable=False)

    main_contact_id = Column(Integer, ForeignKey("users.user_id"))
    lead_auditor_id = Column(Integer, ForeignKey("users.user_id"))

    title = Column(String(200))
    version = Column(String(50), default="V1.0")
    status = Column(String(50))
    classification = Column(String(100))
    firma_adress = Column(String(200))
    date_of_order = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    advisor = Column(String(100))
    observer = Column(String(300))
    goals = Column(VARCHAR(500))
    scope = Column(VARCHAR(500))
    type = Column(String(100))
    dates_and_location = Column(VARCHAR(500))
    comment = Column(VARCHAR(500))
    preassessment = Column(Boolean)
    management_summary = Column(VARCHAR(1000))
    impression_text_area = Column(VARCHAR(1000))
    availability = Column(Integer, nullable=True)
    confidentiality = Column(Integer, nullable=True)
    proto = Column(String(50), nullable=True)
    data = Column(String(50), nullable=True)
    validation = Column(VARCHAR(50), default='incoming')
    # -------------------------
    # Relationships
    # -------------------------

    # One-to-Many: One customer can have many audits
    customer = relationship("Customer", back_populates="audits")

    # One-to-Many: One norm can be applied in many audits
    norm = relationship("Norm", back_populates="audits")

    # One-to-Many (self side): One user can be the main contact for multiple audits
    main_contact = relationship("User",back_populates="managed_audits",foreign_keys=[main_contact_id])

    # One-to-Many (self side): One user can approve multiple audits
    lead_auditor = relationship("User", back_populates="approved_audits",foreign_keys=[lead_auditor_id])

    # One-to-Many: An audit can have multiple audit days
    # audit_days = relationship("AuditDay", back_populates="audit" , cascade="all, delete")

    # Many-to-Many: An audit can involve multiple users (auditors), and each user can be assigned to many audits
    # user_audits = relationship("UserAudit", back_populates="audit")

    # One-to-Many: An audit can have many question responses
    # question_responses = relationship("QuestionResponse", back_populates="audit")