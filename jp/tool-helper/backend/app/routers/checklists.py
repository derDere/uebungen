from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/checklists", tags=["checklists"])


class CreateChecklistFromTemplate(BaseModel):
    tool_id: int
    name: Optional[str] = None


@router.get("/", response_model=List[schemas.CheckList])
def list_checklists(tool_id: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_checklists(db, tool_id=tool_id, skip=skip, limit=limit)


@router.post("/", response_model=schemas.CheckList)
def create_checklist(checklist: schemas.CheckListCreate, db: Session = Depends(get_db)):
    return crud.create_checklist(db, checklist)


@router.post("/from-template/{template_id}", response_model=schemas.CheckList)
def create_checklist_from_template(
    template_id: int,
    data: CreateChecklistFromTemplate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_checklist_from_template(db, data.tool_id, template_id, data.name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{checklist_id}", response_model=schemas.CheckList)
def get_checklist(checklist_id: int, db: Session = Depends(get_db)):
    db_checklist = crud.get_checklist(db, checklist_id)
    if db_checklist is None:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return db_checklist


@router.put("/{checklist_id}", response_model=schemas.CheckList)
def update_checklist(checklist_id: int, checklist: schemas.CheckListUpdate, db: Session = Depends(get_db)):
    db_checklist = crud.update_checklist(db, checklist_id, checklist)
    if db_checklist is None:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return db_checklist


@router.delete("/{checklist_id}")
def delete_checklist(checklist_id: int, db: Session = Depends(get_db)):
    success = crud.delete_checklist(db, checklist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return {"message": "Checklist deleted successfully"}


@router.patch("/{checklist_id}/points/{point_id}/toggle", response_model=schemas.CheckListPoint)
def toggle_point(checklist_id: int, point_id: int, db: Session = Depends(get_db)):
    db_point = crud.toggle_checklist_point(db, point_id)
    if db_point is None:
        raise HTTPException(status_code=404, detail="Point not found")
    return db_point


@router.post("/{checklist_id}/points", response_model=schemas.CheckList)
def add_point_to_checklist(
    checklist_id: int,
    point: schemas.CheckListPointCreate,
    db: Session = Depends(get_db)
):
    db_point = crud.create_checklist_point(db, point)
    db_checklist = crud.add_point_to_checklist(db, checklist_id, db_point.id)
    if db_checklist is None:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return db_checklist


@router.delete("/{checklist_id}/points/{point_id}")
def remove_point_from_checklist(checklist_id: int, point_id: int, db: Session = Depends(get_db)):
    db_checklist = crud.remove_point_from_checklist(db, checklist_id, point_id)
    if db_checklist is None:
        raise HTTPException(status_code=404, detail="Checklist or point not found")
    return {"message": "Point removed from checklist"}


@router.get("/search/{query}")
def search(query: str, db: Session = Depends(get_db)):
    return crud.search_all(db, query)
