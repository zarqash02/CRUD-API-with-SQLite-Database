from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from contextlib import asynccontextmanager


DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Task(Base):
  __tablename__ = "tasks"

  id = Column(Integer, index=True, autoincrement=True, primary_key=True)
  title = Column(String)
  done = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)



class UserResponse(BaseModel):
  id: Optional[int] = None
  title: str
  done: Optional[bool] = False

  class Config:
    orm_mode = True


class TaskRequest(BaseModel):
  title: str
  done: Optional[bool] = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        task_count = db.query(Task).count()
        if task_count == 0:
            default_tasks = [
            Task(title="Task 1", done=False),
            Task(title="Task 2", done=True),
            Task(title="Task 3", done=False)
            ]
            db.add_all(default_tasks)
            db.commit()
        else:
            print(f"Database already has {task_count} tasks. Skipping seeding.")
    finally:
        db.close()
    yield
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }


@app.get("/health")
def isalive():
    return {"status" : "ok"}


@app.get("/tasks", response_model=list[UserResponse])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()



@app.get("/tasks/{id}")
def view_tasks(id: int,db: Session = Depends(get_db)):
   task = db.query(Task).filter(Task.id == id).first()
   if task is None:
       raise HTTPException(status_code=404, detail=f"task {id} does not exist")
   else:
       return {task}



@app.post("/tasks", response_model=UserResponse)
def create_task(task: TaskRequest, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, done=task.done)
    if not new_task.title:
        raise HTTPException(status_code=400, detail="Task title is required")
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return Response(status_code=status.HTTP_201_CREATED, content=f"Task {new_task.id} created successfully")




@app.put("/tasks/{id}")
async def update_task(id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task is None:
       raise HTTPException(status_code=404, detail=f"Task {id} does not exit")
    else:
        task.title = task_update.title if task_update.title is not None else task.title
        task.done = task_update.done if task_update.done is not None else task.done
        db.commit()
        db.refresh(task)
        return {"message":f"task {id} updated successfully"}, task




@app.delete("/tasks/{id}")
async def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {id} does not exit")
    else:
        db.query(Task).filter(Task.id == id).delete()
        db.commit()
        return f"Task {id} has been deleted"