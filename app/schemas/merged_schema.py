from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.page_schema import PageSchema


class MergedSchema(BaseModel):

    pages: list[PageSchema] = Field(default_factory=list)