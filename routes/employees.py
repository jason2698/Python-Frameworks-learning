from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix='/employees',
    tags=['Employees']
)

employees = [
    {'id' : 1, 'name' : "Jason", 'age' : 28},
    {'id' : 2, 'name' : "John", 'age' : 30},
    {'id' : 3, 'name' : "Moses", 'age' : 29}
]   

@router.get('/')
def get_employees():
    return employees

@router.get('/{emp_id}')
def get_employee(emp_id:int):
    emp = list(filter(lambda emp: emp['id'] == emp_id, employees))
    
    if emp is None:
        raise HTTPException(
            status_code=404,
            detail='Product not found'
        )

    return emp
