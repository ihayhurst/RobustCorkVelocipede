
from pydantic import BaseModel

class Config: orm_mode = True

class Details(BaseModel):
	assayId: str
	units: str

class AvailableProperties(BaseModel):
	
	columnType: str
	columnName: str
	fieldName: str
	details: Details

class AvailablePropertiesStruc(AvailableProperties):

	xformat: str

class AdditionalMetadata(BaseModel):

	endpointName: str
	constant: int
	factor: int
	functionType: str
