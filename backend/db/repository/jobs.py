from db.models.jobs import Job
from schemas.jobs import JobCreate
from sqlalchemy.orm import Session


def create_new_job(job: JobCreate, db: Session, owner_id: int) -> Job:
    job_object = Job(**job.dict(), owner_id=owner_id)
    db.add(job_object)
    db.commit()
    db.refresh(job_object)
    return job_object


def retreive_job(id: int, db: Session) -> Job:
    return db.query(Job).get(id)


def list_jobs(db: Session) -> list:
    return db.query(Job).filter(Job.is_active == True).all()


def update_job_by_id(id: int, job: JobCreate, db: Session, owner_id: int) -> int:
    existing_job = db.query(Job).filter(Job.id == id).first()
    if not existing_job:
        return 0
    job_dict = job.dict()
    job_dict.update(owner_id=owner_id)
    db.query(Job).filter(Job.id == id).update(job_dict)
    db.commit()
    return 1


def delete_job_by_id(id: int, db: Session, owner_id):
    existing_job = db.query(Job).filter(Job.id == id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1


def search_job(query: str, db: Session) -> list:
    return db.query(Job).filter(Job.title.contains(query)).all()
