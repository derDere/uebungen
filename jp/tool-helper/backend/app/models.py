from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# Junction table for CheckList and CheckListPoint (many-to-many)
checklist_point_association = Table(
    'check_list_check_list_point',
    Base.metadata,
    Column('check_list_id', Integer, ForeignKey('check_list.id', ondelete='CASCADE'), primary_key=True),
    Column('check_list_point_id', Integer, ForeignKey('check_list_point.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, server_default=func.now())
)

# Junction table for CheckListTemplate and CheckListPointTemplate (many-to-many)
template_point_association = Table(
    'check_list_template_point_template',
    Base.metadata,
    Column('check_list_template_id', Integer, ForeignKey('check_list_template.id', ondelete='CASCADE'), primary_key=True),
    Column('check_list_point_template_id', Integer, ForeignKey('check_list_point_template.id', ondelete='CASCADE'), primary_key=True),
    Column('sort_order', Integer, default=0),
    Column('created_at', DateTime, server_default=func.now())
)


class Tool(Base):
    __tablename__ = "tool"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    checklists = relationship("CheckList", back_populates="tool", cascade="all, delete-orphan")


class CheckListTemplate(Base):
    __tablename__ = "check_list_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    checklists = relationship("CheckList", back_populates="template")
    point_templates = relationship(
        "CheckListPointTemplate",
        secondary=template_point_association,
        back_populates="templates"
    )


class CheckList(Base):
    __tablename__ = "check_list"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    tool_id = Column(Integer, ForeignKey("tool.id", ondelete='CASCADE'), nullable=False)
    check_list_template_id = Column(Integer, ForeignKey("check_list_template.id", ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tool = relationship("Tool", back_populates="checklists")
    template = relationship("CheckListTemplate", back_populates="checklists")
    points = relationship(
        "CheckListPoint",
        secondary=checklist_point_association,
        back_populates="checklists"
    )


class CheckListPointTemplate(Base):
    __tablename__ = "check_list_point_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datatype = Column(String, default="text")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    templates = relationship(
        "CheckListTemplate",
        secondary=template_point_association,
        back_populates="point_templates"
    )
    points = relationship("CheckListPoint", back_populates="point_template")


class CheckListPoint(Base):
    __tablename__ = "check_list_point"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, default="active")
    is_checked = Column(Boolean, default=False)
    check_list_point_template_id = Column(Integer, ForeignKey("check_list_point_template.id", ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    point_template = relationship("CheckListPointTemplate", back_populates="points")
    checklists = relationship(
        "CheckList",
        secondary=checklist_point_association,
        back_populates="points"
    )
