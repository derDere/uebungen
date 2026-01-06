from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Tool Schemas
class ToolBase(BaseModel):
    name: str
    status: str = "active"


class ToolCreate(ToolBase):
    pass


class ToolUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None


class Tool(ToolBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# CheckListPointTemplate Schemas
class CheckListPointTemplateBase(BaseModel):
    name: str
    datatype: str = "text"


class CheckListPointTemplateCreate(CheckListPointTemplateBase):
    pass


class CheckListPointTemplateUpdate(BaseModel):
    name: Optional[str] = None
    datatype: Optional[str] = None


class CheckListPointTemplate(CheckListPointTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# CheckListTemplate Schemas
class CheckListTemplateBase(BaseModel):
    name: str
    status: str = "active"


class CheckListTemplateCreate(CheckListTemplateBase):
    pass


class CheckListTemplateUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None


class CheckListTemplate(CheckListTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime
    point_templates: List[CheckListPointTemplate] = []

    class Config:
        from_attributes = True


# CheckListPoint Schemas
class CheckListPointBase(BaseModel):
    name: str
    status: str = "active"
    is_checked: bool = False


class CheckListPointCreate(CheckListPointBase):
    check_list_point_template_id: Optional[int] = None


class CheckListPointUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    is_checked: Optional[bool] = None


class CheckListPoint(CheckListPointBase):
    id: int
    check_list_point_template_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# CheckList Schemas
class CheckListBase(BaseModel):
    name: str
    status: str = "active"


class CheckListCreate(CheckListBase):
    tool_id: int
    check_list_template_id: Optional[int] = None


class CheckListUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None


class CheckList(CheckListBase):
    id: int
    tool_id: int
    check_list_template_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    points: List[CheckListPoint] = []

    class Config:
        from_attributes = True


# Extended schemas with relationships
class ToolWithChecklists(Tool):
    checklists: List[CheckList] = []

    class Config:
        from_attributes = True
