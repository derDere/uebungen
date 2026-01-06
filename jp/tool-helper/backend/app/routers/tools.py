from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("/", response_model=List[schemas.Tool])
def list_tools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tools(db, skip=skip, limit=limit)


@router.post("/", response_model=schemas.Tool)
def create_tool(tool: schemas.ToolCreate, db: Session = Depends(get_db)):
    return crud.create_tool(db, tool)


@router.get("/{tool_id}", response_model=schemas.ToolWithChecklists)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    db_tool = crud.get_tool(db, tool_id)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool


@router.put("/{tool_id}", response_model=schemas.Tool)
def update_tool(tool_id: int, tool: schemas.ToolUpdate, db: Session = Depends(get_db)):
    db_tool = crud.update_tool(db, tool_id, tool)
    if db_tool is None:
        raise HTTPException(status_code=404, detail="Tool not found")
    return db_tool


@router.delete("/{tool_id}")
def delete_tool(tool_id: int, db: Session = Depends(get_db)):
    success = crud.delete_tool(db, tool_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"message": "Tool deleted successfully"}
