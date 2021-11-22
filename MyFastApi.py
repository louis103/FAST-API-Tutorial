from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "grade": "grade 3"
    },
    2: {
        "name": "Esther",
        "age": 21,
        "grade": "grade 4"
    }
}
shopping_list = {
    1: {
        "item": "Sugar",
        "price": 105.78
    },
    2:
        {
            "item": "Salt",
            "price": 15.78
        }
}


class Student(BaseModel):
    name: str
    age: int
    grade: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None


class Items(BaseModel):
    item: str
    price: float


# create endpoint(one end of a communication channel)
@app.get("/")  # home
def home():
    return {"name": "First Data"}


# endpoint params/Path
@app.get("/get_student/{student_id}")
def get_student(student_id: int = Path(None, description="The ID of the student you wanna view", gt=0, lt=10)):
    return students[student_id]


# query params
@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found!"}


# combining Path and Query Params
# request body and the post method

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Students exists"}

    students[student_id] = student
    return students[student_id]


# put method
@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Such a student does not exist!"}

    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.grade != None:
        students[student_id].grade = student.grade

    # students[student_id] = student
    return students[student_id]

# delete method
@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error" : "Student does not exist!"}
    del students[student_id]
    return {"Message": f"Student at id {student_id} was deleted!"}
