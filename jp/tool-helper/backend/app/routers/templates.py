from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/templates", tags=["templates"])


# CheckList Template endpoints
@router.get("/checklist", response_model=List[schemas.CheckListTemplate])
def list_checklist_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_checklist_templates(db, skip=skip, limit=limit)


@router.post("/checklist", response_model=schemas.CheckListTemplate)
def create_checklist_template(template: schemas.CheckListTemplateCreate, db: Session = Depends(get_db)):
    return crud.create_checklist_template(db, template)


@router.get("/checklist/{template_id}", response_model=schemas.CheckListTemplate)
def get_checklist_template(template_id: int, db: Session = Depends(get_db)):
    db_template = crud.get_checklist_template(db, template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template


@router.put("/checklist/{template_id}", response_model=schemas.CheckListTemplate)
def update_checklist_template(
    template_id: int,
    template: schemas.CheckListTemplateUpdate,
    db: Session = Depends(get_db)
):
    db_template = crud.update_checklist_template(db, template_id, template)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template


@router.delete("/checklist/{template_id}")
def delete_checklist_template(template_id: int, db: Session = Depends(get_db)):
    success = crud.delete_checklist_template(db, template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template deleted successfully"}


@router.post("/checklist/{template_id}/points/{point_template_id}", response_model=schemas.CheckListTemplate)
def add_point_template_to_checklist_template(
    template_id: int,
    point_template_id: int,
    db: Session = Depends(get_db)
):
    db_template = crud.add_point_template_to_template(db, template_id, point_template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template or point template not found")
    return db_template


@router.delete("/checklist/{template_id}/points/{point_template_id}")
def remove_point_template_from_checklist_template(
    template_id: int,
    point_template_id: int,
    db: Session = Depends(get_db)
):
    db_template = crud.remove_point_template_from_template(db, template_id, point_template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template or point template not found")
    return {"message": "Point template removed from checklist template"}


# Point Template endpoints
@router.get("/point", response_model=List[schemas.CheckListPointTemplate])
def list_point_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_point_templates(db, skip=skip, limit=limit)


@router.post("/point", response_model=schemas.CheckListPointTemplate)
def create_point_template(template: schemas.CheckListPointTemplateCreate, db: Session = Depends(get_db)):
    return crud.create_point_template(db, template)


@router.get("/point/{template_id}", response_model=schemas.CheckListPointTemplate)
def get_point_template(template_id: int, db: Session = Depends(get_db)):
    db_template = crud.get_point_template(db, template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Point template not found")
    return db_template


@router.put("/point/{template_id}", response_model=schemas.CheckListPointTemplate)
def update_point_template(
    template_id: int,
    template: schemas.CheckListPointTemplateUpdate,
    db: Session = Depends(get_db)
):
    db_template = crud.update_point_template(db, template_id, template)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Point template not found")
    return db_template


@router.delete("/point/{template_id}")
def delete_point_template(template_id: int, db: Session = Depends(get_db)):
    success = crud.delete_point_template(db, template_id)
    if not success:
        raise HTTPException(status_code=404, detail="Point template not found")
    return {"message": "Point template deleted successfully"}
