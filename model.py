from pydantic import BaseModel, Field

class Product(BaseModel):
    id : int
    name : str = Field(min_length=3)
    description : str
    price : float = Field(gt=0)
    quantity : int

