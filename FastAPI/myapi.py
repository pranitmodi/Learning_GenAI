from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

# GET - Read Data
# POST - Insert Data
# PUT - Update Data
# DELETE - Delete Data

students = {
    1: {
        "name": "john",
        "age": 17,
        "year": "year 12"
    },
    2: {
        "name": "doe",
        "age": 18,
        "year": "year 13"
    },
    3: {
        "name": "jane",
        "age": 17,
        "year": "year 10"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

# GET request

@app.get("/")
def index():
    return {"name": "API"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student you want to view", gt=0)):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    return students[student_id]

@app.get("/get-by-name") # will work for /get-by-name?name=john
def get_student(*, name: Optional[str] = None, test: int): # =None to make it optional
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}

@app.get("/search/{student_id}") # query and path parameter
def search_student(student_id: int, student_name: str):
        if students[student_id]["name"] == student_name:
            return students[student_id]
        return {"Data": "Not Found"}

# POST request 

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    students[student_id] = student
    return {"Student Created": student}

# PUT request

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    if student.name != None:
        students[student_id]["name"] = student.name

    if student.age != None:
        students[student_id]["age"] = student.age

    if student.year != None:
        students[student_id]["year"] = student.year

    return {"Student Updated": students[student_id]}

# DELETE request

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    del students[student_id]
    return {"Message": "Student Deleted"}