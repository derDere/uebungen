from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import csv
import json
import yaml
from io import StringIO
from . import models, schemas


# Tool CRUD
def get_tools(db: Session, skip: int = 0, limit: int = 100) -> List[models.Tool]:
    return db.query(models.Tool).offset(skip).limit(limit).all()


def get_tool(db: Session, tool_id: int) -> Optional[models.Tool]:
    return db.query(models.Tool).filter(models.Tool.id == tool_id).first()


def create_tool(db: Session, tool: schemas.ToolCreate) -> models.Tool:
    db_tool = models.Tool(**tool.model_dump())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool


def update_tool(db: Session, tool_id: int, tool: schemas.ToolUpdate) -> Optional[models.Tool]:
    db_tool = get_tool(db, tool_id)
    if db_tool:
        update_data = tool.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tool, key, value)
        db.commit()
        db.refresh(db_tool)
    return db_tool


def delete_tool(db: Session, tool_id: int) -> bool:
    db_tool = get_tool(db, tool_id)
    if db_tool:
        db.delete(db_tool)
        db.commit()
        return True
    return False


# CheckList CRUD
def get_checklists(db: Session, tool_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[models.CheckList]:
    query = db.query(models.CheckList)
    if tool_id:
        query = query.filter(models.CheckList.tool_id == tool_id)
    return query.offset(skip).limit(limit).all()


def get_checklist(db: Session, checklist_id: int) -> Optional[models.CheckList]:
    return db.query(models.CheckList).filter(models.CheckList.id == checklist_id).first()


def create_checklist(db: Session, checklist: schemas.CheckListCreate) -> models.CheckList:
    db_checklist = models.CheckList(**checklist.model_dump())
    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)
    return db_checklist


def create_checklist_from_template(db: Session, tool_id: int, template_id: int, name: Optional[str] = None) -> models.CheckList:
    template = db.query(models.CheckListTemplate).filter(models.CheckListTemplate.id == template_id).first()
    if not template:
        raise ValueError("Template not found")

    checklist_name = name or f"{template.name} - Instance"
    db_checklist = models.CheckList(
        name=checklist_name,
        tool_id=tool_id,
        check_list_template_id=template_id,
        status=template.status
    )
    db.add(db_checklist)
    db.flush()

    for point_template in template.point_templates:
        db_point = models.CheckListPoint(
            name=point_template.name,
            status="active",
            is_checked=False,
            check_list_point_template_id=point_template.id
        )
        db.add(db_point)
        db.flush()
        db_checklist.points.append(db_point)

    db.commit()
    db.refresh(db_checklist)
    return db_checklist


def update_checklist(db: Session, checklist_id: int, checklist: schemas.CheckListUpdate) -> Optional[models.CheckList]:
    db_checklist = get_checklist(db, checklist_id)
    if db_checklist:
        update_data = checklist.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_checklist, key, value)
        db.commit()
        db.refresh(db_checklist)
    return db_checklist


def delete_checklist(db: Session, checklist_id: int) -> bool:
    db_checklist = get_checklist(db, checklist_id)
    if db_checklist:
        db.delete(db_checklist)
        db.commit()
        return True
    return False


def add_point_to_checklist(db: Session, checklist_id: int, point_id: int) -> Optional[models.CheckList]:
    db_checklist = get_checklist(db, checklist_id)
    db_point = get_checklist_point(db, point_id)
    if db_checklist and db_point:
        if db_point not in db_checklist.points:
            db_checklist.points.append(db_point)
            db.commit()
            db.refresh(db_checklist)
    return db_checklist


def remove_point_from_checklist(db: Session, checklist_id: int, point_id: int) -> Optional[models.CheckList]:
    db_checklist = get_checklist(db, checklist_id)
    db_point = get_checklist_point(db, point_id)
    if db_checklist and db_point:
        if db_point in db_checklist.points:
            db_checklist.points.remove(db_point)
            db.commit()
            db.refresh(db_checklist)
    return db_checklist


# CheckListPoint CRUD
def get_checklist_points(db: Session, skip: int = 0, limit: int = 100) -> List[models.CheckListPoint]:
    return db.query(models.CheckListPoint).offset(skip).limit(limit).all()


def get_checklist_point(db: Session, point_id: int) -> Optional[models.CheckListPoint]:
    return db.query(models.CheckListPoint).filter(models.CheckListPoint.id == point_id).first()


def create_checklist_point(db: Session, point: schemas.CheckListPointCreate) -> models.CheckListPoint:
    db_point = models.CheckListPoint(**point.model_dump())
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


def update_checklist_point(db: Session, point_id: int, point: schemas.CheckListPointUpdate) -> Optional[models.CheckListPoint]:
    db_point = get_checklist_point(db, point_id)
    if db_point:
        update_data = point.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_point, key, value)
        db.commit()
        db.refresh(db_point)
    return db_point


def toggle_checklist_point(db: Session, point_id: int) -> Optional[models.CheckListPoint]:
    db_point = get_checklist_point(db, point_id)
    if db_point:
        db_point.is_checked = not db_point.is_checked
        db.commit()
        db.refresh(db_point)
    return db_point


def delete_checklist_point(db: Session, point_id: int) -> bool:
    db_point = get_checklist_point(db, point_id)
    if db_point:
        db.delete(db_point)
        db.commit()
        return True
    return False


# CheckListTemplate CRUD
def get_checklist_templates(db: Session, skip: int = 0, limit: int = 100) -> List[models.CheckListTemplate]:
    return db.query(models.CheckListTemplate).offset(skip).limit(limit).all()


def get_checklist_template(db: Session, template_id: int) -> Optional[models.CheckListTemplate]:
    return db.query(models.CheckListTemplate).filter(models.CheckListTemplate.id == template_id).first()


def create_checklist_template(db: Session, template: schemas.CheckListTemplateCreate) -> models.CheckListTemplate:
    db_template = models.CheckListTemplate(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


def update_checklist_template(db: Session, template_id: int, template: schemas.CheckListTemplateUpdate) -> Optional[models.CheckListTemplate]:
    db_template = get_checklist_template(db, template_id)
    if db_template:
        update_data = template.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_template, key, value)
        db.commit()
        db.refresh(db_template)
    return db_template


def delete_checklist_template(db: Session, template_id: int) -> bool:
    db_template = get_checklist_template(db, template_id)
    if db_template:
        db.delete(db_template)
        db.commit()
        return True
    return False


def add_point_template_to_template(db: Session, template_id: int, point_template_id: int) -> Optional[models.CheckListTemplate]:
    db_template = get_checklist_template(db, template_id)
    db_point_template = get_point_template(db, point_template_id)
    if db_template and db_point_template:
        if db_point_template not in db_template.point_templates:
            db_template.point_templates.append(db_point_template)
            db.commit()
            db.refresh(db_template)
    return db_template


def remove_point_template_from_template(db: Session, template_id: int, point_template_id: int) -> Optional[models.CheckListTemplate]:
    db_template = get_checklist_template(db, template_id)
    db_point_template = get_point_template(db, point_template_id)
    if db_template and db_point_template:
        if db_point_template in db_template.point_templates:
            db_template.point_templates.remove(db_point_template)
            db.commit()
            db.refresh(db_template)
    return db_template


# CheckListPointTemplate CRUD
def get_point_templates(db: Session, skip: int = 0, limit: int = 100) -> List[models.CheckListPointTemplate]:
    return db.query(models.CheckListPointTemplate).offset(skip).limit(limit).all()


def get_point_template(db: Session, template_id: int) -> Optional[models.CheckListPointTemplate]:
    return db.query(models.CheckListPointTemplate).filter(models.CheckListPointTemplate.id == template_id).first()


def create_point_template(db: Session, template: schemas.CheckListPointTemplateCreate) -> models.CheckListPointTemplate:
    db_template = models.CheckListPointTemplate(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


def update_point_template(db: Session, template_id: int, template: schemas.CheckListPointTemplateUpdate) -> Optional[models.CheckListPointTemplate]:
    db_template = get_point_template(db, template_id)
    if db_template:
        update_data = template.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_template, key, value)
        db.commit()
        db.refresh(db_template)
    return db_template


def delete_point_template(db: Session, template_id: int) -> bool:
    db_template = get_point_template(db, template_id)
    if db_template:
        db.delete(db_template)
        db.commit()
        return True
    return False


# Search functionality
def search_all(db: Session, query: str):
    tools = db.query(models.Tool).filter(models.Tool.name.contains(query)).all()
    checklists = db.query(models.CheckList).filter(models.CheckList.name.contains(query)).all()
    points = db.query(models.CheckListPoint).filter(models.CheckListPoint.name.contains(query)).all()

    return {
        "tools": tools,
        "checklists": checklists,
        "points": points
    }


# Export functionality
def export_to_json(db: Session) -> str:
    data = {
        "tools": [schemas.Tool.model_validate(t).model_dump() for t in get_tools(db, limit=1000)],
        "checklists": [schemas.CheckList.model_validate(c).model_dump() for c in get_checklists(db, limit=1000)],
        "checklist_templates": [schemas.CheckListTemplate.model_validate(t).model_dump() for t in get_checklist_templates(db, limit=1000)],
        "point_templates": [schemas.CheckListPointTemplate.model_validate(p).model_dump() for p in get_point_templates(db, limit=1000)]
    }
    return json.dumps(data, indent=2, default=str)


def export_to_yaml(db: Session) -> str:
    data = {
        "tools": [schemas.Tool.model_validate(t).model_dump() for t in get_tools(db, limit=1000)],
        "checklists": [schemas.CheckList.model_validate(c).model_dump() for c in get_checklists(db, limit=1000)],
        "checklist_templates": [schemas.CheckListTemplate.model_validate(t).model_dump() for t in get_checklist_templates(db, limit=1000)],
        "point_templates": [schemas.CheckListPointTemplate.model_validate(p).model_dump() for p in get_point_templates(db, limit=1000)]
    }
    return yaml.dump(data, default_flow_style=False)


def export_to_csv(db: Session) -> str:
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Type", "ID", "Name", "Status", "Additional Info"])

    for tool in get_tools(db, limit=1000):
        writer.writerow(["Tool", tool.id, tool.name, tool.status, ""])

    for checklist in get_checklists(db, limit=1000):
        writer.writerow(["CheckList", checklist.id, checklist.name, checklist.status, f"Tool ID: {checklist.tool_id}"])

    for point in get_checklist_points(db, limit=1000):
        writer.writerow(["CheckListPoint", point.id, point.name, point.status, f"Checked: {point.is_checked}"])

    return output.getvalue()


def export_to_markdown(db: Session) -> str:
    md = "# Tool Helper Export\n\n"

    md += "## Tools\n\n"
    for tool in get_tools(db, limit=1000):
        md += f"### {tool.name}\n"
        md += f"- **ID**: {tool.id}\n"
        md += f"- **Status**: {tool.status}\n\n"

        tool_checklists = get_checklists(db, tool_id=tool.id)
        if tool_checklists:
            md += "#### Checklists:\n"
            for checklist in tool_checklists:
                md += f"- {checklist.name} (Status: {checklist.status})\n"
                for point in checklist.points:
                    checked = "✓" if point.is_checked else "☐"
                    md += f"  - {checked} {point.name}\n"
            md += "\n"

    md += "## Templates\n\n"
    for template in get_checklist_templates(db, limit=1000):
        md += f"### {template.name}\n"
        md += f"- **ID**: {template.id}\n"
        md += f"- **Status**: {template.status}\n"
        if template.point_templates:
            md += "- **Point Templates**:\n"
            for pt in template.point_templates:
                md += f"  - {pt.name} ({pt.datatype})\n"
        md += "\n"

    return md
