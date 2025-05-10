from pydantic import BaseModel, Field
class AuditorResponse(BaseModel):
    id: str = Field(..., alias="_id")
    usuario: str

    class Config:
        allow_population_by_field_name = True