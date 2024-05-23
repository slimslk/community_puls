from pydantic import BaseModel, Field


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=15)
    category_id: int = Field(..., description="You should to provide Category ID")


class QuestionResponse(BaseModel):
    id: int
    text: str
    category_name: str

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3)


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
