from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from .. import crud
from ..database import get_db

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/json", response_class=PlainTextResponse)
def export_json(db: Session = Depends(get_db)):
    return crud.export_to_json(db)


@router.get("/yaml", response_class=PlainTextResponse)
def export_yaml(db: Session = Depends(get_db)):
    return crud.export_to_yaml(db)


@router.get("/csv", response_class=PlainTextResponse)
def export_csv(db: Session = Depends(get_db)):
    return crud.export_to_csv(db)


@router.get("/markdown", response_class=PlainTextResponse)
def export_markdown(db: Session = Depends(get_db)):
    return crud.export_to_markdown(db)
