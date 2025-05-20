from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern="^[a-f\d]{24}$")]

class AuditorExterno(BaseModel):
    id: str = Field(..., alias="_id", pattern="^[a-f\d]{24}$")
    nombre: str

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
