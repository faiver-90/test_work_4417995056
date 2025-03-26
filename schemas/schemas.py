from typing import List

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    success: bool
    error: str


class SuccessFileSchema(BaseModel):
    success: bool


class CountSchema(BaseModel):
    count: int


class AttributesOutSchema(BaseModel):
    attributes: List[str]
