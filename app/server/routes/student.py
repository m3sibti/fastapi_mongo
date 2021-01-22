from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from app.server.database import *
from app.server.models.student import *

router = APIRouter()


# Add student
@router.post('/', response_description='Student data added into database')
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    return ResponseModel(new_student, "Student added Successfully")


# Read All Students
@router.get('/', response_description='Students data retrieved successfully')
async def get_students():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "Students data retrieved successfully")
    return ResponseModel(students, "Empty list returned")


# Read Student with ID
@router.get('/{id}', response_description='Students data retrieved successfully')
async def get_student_data(id):
    student = await retrieve_student(id)
    if student:
        return ResponseModel(student, "Student data retrieved successfully")
    return ErrorResponseModel("An error occurred", 404, "Student doesn't exist.")


# Update Student with ID
@router.put('/{id}')
async def update_student_data(id: str, req: UpdateStudentModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await update_student(id, req)
    if updated_student:
        return ResponseModel(
            f"Student with ID: {id} name update is successful",
            "Student name updated successfully",
        )
    return ErrorResponseModel("An error occurred", 404, "Student updating error.")


@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id: str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return ResponseModel(
            "Student with ID: {} removed".format(id), "Student deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
    )
