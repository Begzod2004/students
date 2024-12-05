from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Models
class Group(BaseModel):
    direction: str
    group_number: int
    room_number: int

class Student(BaseModel):
    name: str
    lastname: str
    address: str
    group_id: int

# In-memory storage
groups: List[Group] = []
students: List[Student] = []
group_students = {

}
# Endpoints for Groups
@app.post("/groups/")
def create_group(group: Group):
    groups.append(group)
    return group

@app.get("/groups/")
def get_groups():
    return groups

# Endpoints for Students
@app.post("/students/", response_model=Student)
def create_student(student: Student, group_id: int):
    students.append(student)
    for i in groups:
        if i.group_number == group_id:
            group_students[i.group_number] = list(student)
            return f"{group_students}"
        else:
            return f"{group_id} topilmadi"
    return f"{student} talaba qo'shildi"
        

@app.get("/students/", response_model=List[Student])
def get_students():
    return students

@app.get("/get_student")
def get_student_by_name(name: str, l_name):
    for i in students:
        if i.name == name and i.lastname == l_name:
            return f"{i}"
        else:
            return f"topilmadi bunday talaba"


# Get students by group ID
@app.get("/groups/{group_id}/students/", response_model=List[Student])
def get_students_by_group(group_id: int):
    group_students = [student for student in students if student.group_id == group_id]
    if not any(group.id == group_id for group in groups):
        raise HTTPException(status_code=404, detail="Group not found")
    return group_students 
