from fastapi import APIRouter, Depends, status, HTTPException
from app.database.connections import get_db
from app.schemas.tasks_schema import TaskCreate, TaskResponse, TaskUpdate
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.task import create_new_task, get_tasks, get_task_by_id, get_all_tasks_and_their_user, update_task, delete_task
from app.services.auth import get_current_user
import uuid


router = APIRouter(prefix="/Tasks", tags=["tasks"])


@router.post("/task_create", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(body: TaskCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_task = await create_new_task(body=body, user=user, db=db)

    return new_task


@router.get("/tasks", response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
async def get_user_tasks(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    tasks = await get_tasks(user=user, db=db)

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User didn't create tasks"
        )

    return tasks

@router.get("/task/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_user_task_by_task_id(task_id: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    task = await get_task_by_id(task_id=task_id, user=user, db=db)

    return task


@router.get("/tasks_and_their_users", status_code=status.HTTP_200_OK)
async def get_tasks_and_users(db: AsyncSession = Depends(get_db)):

    tasks = await get_all_tasks_and_their_user(db=db)

    return tasks


@router.patch("/update_task/{task_id}", status_code=status.HTTP_200_OK)
async def update_task_by_id(task_id: uuid.UUID, body: TaskUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    updatedTask = await update_task(task_id=task_id, body=body, user=user, db=db)

    return {"updated task" : updatedTask._asdict()}



@router.delete("/delete_task{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(task_id: uuid.UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    return await delete_task(task_id=task_id, user=user, db=db)





