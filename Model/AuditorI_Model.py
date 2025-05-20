from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern="^[a-f\d]{24}$")]

class AuditorInterno(BaseModel):
    id: ObjectIdStr = Field(alias="_id")
    nombre: str
    compañia: str

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
