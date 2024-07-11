from fastapi import FastAPI,Depends,HTTPException,status
from .models import Dept
from .schemas import BaseDept
from .database import SessionLocal,engine,Base
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import datetime,timedelta,date

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@app.post('/api/depts',tags = ['depts'])
async def create_depts(dept:BaseDept,db:db_dependency):
    try:
        dept=Dept(dept_type = dept.dept_type,
                  first_name = dept.first_name,
                  last_name = dept.last_name,
                  price_dept =dept.price_dept,
                  day = dept.day,
                  type_curr = dept.type_curr,
                  description = dept.description,
                  from_time = dept.from_time,
                  to_time = timedelta(days=dept.day)+dept.from_time,
                  paid = dept.paid)
        db.add(dept)
        db.commit()
        db.refresh(dept)
        return dept
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail='Your credentials not correnct')
    
@app.delete('/api/depts/{item_id}',tags = ['depts'])
async def delete_depts(db:db_dependency,item_id):
    dept_id = db.query(Dept).filter(Dept.id == item_id).first()
    db.delete(dept_id)
    db.commit()
    return {'status':'success',
            'message':'Deleted succfully'}


@app.patch('/api/depts/update/{item_id}',tags = ['depts'])
async def update_depts(db:db_dependency,item_id,dept:BaseDept):
    dept_id = db.query(Dept).filter(Dept.id == item_id).first()
    if dept_id:
        for key,val in dept.dict(exclude_unset=True).items():
            setattr(dept_id,key,val)
    
        db.commit()
    return {'dept':dept,
            'message':'Successfully updated'}

@app.get('/depts/list',tags = ['depts'])
async def list_depts(db:db_dependency):
    debts_by_user = 0
    depts_own = 0
    list_depts = db.query(Dept).all()
    for dept in list_depts:
        if dept.dept_type =='owned_by_me':
            debts_by_user += dept.price_dept
        elif dept.dept_type =='owned_to_me':
            depts_own += dept.price_dept


    response_model = {
        'dept':list_depts,
        'qarzdorlik':depts_own,
        'qariborlar':debts_by_user

    }
    return response_model

@app.get('/api/depts/',tags = ['users by dept'])
async def get_by_typedept(db:db_dependency,dept_type:str|None=None):
    total_sum = 0
    if dept_type:
        list_depts = db.query(Dept).filter(Dept.dept_type == dept_type).all()
        for dept in list_depts:
            total_sum += dept.price_dept
        if list_depts:
            return {'depts':list_depts,
                    'total_price':total_sum}
    return {'messgae':'no response'}

