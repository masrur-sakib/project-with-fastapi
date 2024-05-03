from fastapi import FastAPI, Path 
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "sakib",
        "age": 28,
        "className": "class 5"
    },
    2: {
        "name": "zoraiz",
        "age": 5,
        "className": "class 1"
    },
    3: {
        "name": "jobaida",
        "age": 10,
        "className": "class 3"
    }
}

class Student(BaseModel):
    name: str
    age: int
    className: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    className: Optional[str] = None

# ******* GET METHOD ********
# ---------------------------

@app.get("/")
def root():
    return {"name": "fastapi server"}

# Path parameter
@app.get("/student/{student_id}")
def getStudentInfo(student_id: int = Path(description="The Id of the student.", gt=0)):
    if student_id not in students:
        return {"status": 404, "msg": "Not Found"}
    
    return students[student_id]

# Query parameter - required
@app.get("/student")
def getStudentInfo(name: str):
    for student_id in students:
        if(students[student_id]["name"] == name):
            return students[student_id]
    return {"status": 404, "msg": "data not found"}

# Query parameter - optional
@app.get("/student-optional")
def getStudentInfo(name: Optional[str] = None):
    for student_id in students:
        if(students[student_id]["name"] == name):
            return students[student_id]
    return {"status": 404, "msg": "data not found"}

# Multiple Query parameter - optional, required
@app.get("/student-multi")
def getStudentInfo(*, name: Optional[str] = None, id: int): # first parameter can't be optional, that's why using asterisk *
    for student_id in students:
        if(students[student_id]["name"] == name):
            return students[student_id]
    return {"status": 404, "msg": "data not found"}

# Multiple Query parameter - optional, required with path parameter
@app.get("/student-multi/{student_id}")
def getStudentInfo(*, student_id: int, name: Optional[str] = None, className: str): # first parameter can't be optional, that's why using asterisk *
    for student_id in students:
        if(students[student_id]["name"] == name):
            return students[student_id]
    return {"status": 404, "msg": "data not found"}

# ******* POST METHOD ********
# ----------------------------

@app.post("/add-student")
def addStudent(student: Student):
    student_id = len(students) + 1
    students[student_id] = student
    return students

# ******* PUT METHOD ********
# ----------------------------

@app.put("/update-student/{student_id}")
def updateStudent(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"status": 404, "msg": "Not Found"}
    
    if student.name != None:
        students[student_id]["name"] = student.name
    if student.age != None:
        students[student_id]["age"] = student.age
    if student.className != None:
        students[student_id]["className"] = student.className
        
    return students

# ******* DELETE METHOD ********
# ----------------------------

@app.delete("/delete-student/{student_id}")
def deleteStudent(student_id: int):
    if student_id not in students:
        return {"status": 404, "msg": "Not Found"}
    
    del students[student_id]
    
    return {
        "msg": "student deleted successfully",
        "data": students
    }
        