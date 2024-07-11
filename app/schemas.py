from pydantic import BaseModel

from datetime import date


class BaseDept(BaseModel):
    dept_type:str
    first_name:str
    last_name:str
    price_dept:float
    day:int
    type_curr:str
    description:str
    from_time:date
    to_time:date
    paid:bool|None = False
    

