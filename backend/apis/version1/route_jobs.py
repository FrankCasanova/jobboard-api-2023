from typing import List

from .apis.version1.route_login import get_current_user_from_token
from .db.models.users import User
from .db.repository.jobs import create_new_job
from .db.repository.jobs import delete_job_by_id
from .db.repository.jobs import list_jobs
from .db.repository.jobs import retreive_job
from .db.repository.jobs import update_job_by_id
from .db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from .schemas.jobs import JobCreate
from .schemas.jobs import ShowJob
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create-job/", response_model=ShowJob)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    current_user = 1
    job = create_new_job(job=job, db=db, owner_id=current_user)
    return job


# if we keep just "{id}" . it would stat catching all routes
@router.get("/get/{id}", response_model=ShowJob)
def read_job(id: int, db: Session = Depends(get_db)):
    job = retreive_job(id=id, db=db)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with this id {id} does not exist",
        )
    return job


@router.get("/all", response_model=List[ShowJob])  # new
def read_jobs(db: Session = Depends(get_db)):
    jobs = list_jobs(db=db)
    return jobs


@router.put("/update/{id}")  # new
def update_job(id: int, job: JobCreate, db: Session = Depends(get_db)):
    current_user = 1
    message = update_job_by_id(id=id, job=job, db=db, owner_id=current_user)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with id {id} not found",
        )
    return {"msg": "Successfully updated data."}


@router.delete("/delete/{id}")
def delete_job(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    job = retreive_job(id=id, db=db)
    if not job:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with {id} does not exist",
        )
    print(job.owner_id, current_user.id, current_user.is_superuser)
    if job.owner_id == current_user.id or current_user.is_superuser:
        delete_job_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not permitted!!!!",
    )
