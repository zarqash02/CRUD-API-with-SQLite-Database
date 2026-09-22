from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
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