
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db import Base

class Rule(Base):
    """Stores mlox rules (Order, Conflict, Requires, NearStart, NearEnd, Patch, etc.)."""
    __tablename__ = "rules"

    id              = Column(Integer, primary_key=True, index=True)
    rule_type       = Column(String, nullable=False)    # [Order], [Conflict], [Requires], etc.
    mod_name        = Column(String, nullable=False)    # The main mod this rule applies to
    target_mod      = Column(String, nullable=True)     # Optional secondary mod
    severity        = Column(String, nullable=True)     # Conflict severity (Low, Medium, High)
    priority_level  = Column(Integer, nullable=True)    # 1 (!), 2 (!!), 3 (!!!) for highlighting
    section         = Column(String, nullable=True)     # The @SectionName grouping
    reference       = Column(Text, nullable=True)       # Stores the (Ref: ) source information
    notes           = Column(Text, nullable=True)       # User notes

class Mod(Base):
    """Stores mod metadata (installed mods & Nexus lookups)."""
    __tablename__ = "mods"

    id = Column(Integer, primary_key=True, index=True)
    mod_name        = Column(String, nullable=False, unique=True)
    mod_hash        = Column(String, unique=True, nullable=True)        # Optional file hash
    source          = Column(String, nullable=True)                     # Local or Nexus
    last_updated    = Column(String, nullable=True)                     # Timestamp

class Dependency(Base):
    """Stores mod-to-mod dependencies."""
    __tablename__ = "dependencies"

    id              = Column(Integer, primary_key=True, index=True)
    mod_id          = Column(Integer, ForeignKey("mods.id"), nullable=False)
    depends_on      = Column(Integer, ForeignKey("mods.id"), nullable=False)

    mod             = relationship("Mod", foreign_keys=[mod_id])
    required_mod    = relationship("Mod", foreign_keys=[depends_on])

class Predicate(Base):
    """Stores predicates like DESC, SIZE, VER for advanced rule filtering."""
    __tablename__ = "predicates"

    id              = Column(Integer, primary_key=True, index=True)
    rule_id         = Column(Integer, ForeignKey("rules.id"), nullable=False)
    predicate_type  = Column(String, nullable=False)                    # DESC, SIZE, VER, etc.
    predicate_value = Column(String, nullable=False)                    # The associated value

    rule = relationship("Rule", back_populates="predicates")


Rule.predicates = relationship("Predicate", back_populates="rule", cascade="all, delete-orphan")
