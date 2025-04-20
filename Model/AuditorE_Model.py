from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern="^[a-f\d]{24}$")]

class AuditorExterno(BaseModel):
    id: ObjectIdStr = Field(alias="_id")
    nombre: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
