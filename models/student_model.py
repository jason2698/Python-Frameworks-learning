from pydantic import BaseModel

class Student(BaseModel):
    student_id : int
    name : str
    age : int
    course : str