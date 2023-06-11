# models.py

from pydantic import BaseModel, Field
from typing import List, Optional

class Transformation(BaseModel):
    constant: int
    factor: int
    functionType: str

class Endpoint(BaseModel):
    endpointName: str
    transformation: Transformation

class AdditionalMetadata(BaseModel):
    cerellaEndpoints: List[Endpoint]


class Details(BaseModel):
    assayId: str
    units: str
    format: Optional[str]

class AvailableProperties(BaseModel):
    columnType: str
    columnName: str
    fieldName: str
    details: Details


class DataModel(BaseModel):
    database: str
    name: str
    connection: str
    idColumn: str
    template: str
    cartridgeColumn: Optional[str] = Field(..., nullable=True)
    chemistryColumn: str
    sourceId: str
    additionalMetadata: AdditionalMetadata
    availableProperties: List[AvailableProperties]