from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import and_


from app.schemas.tasks_schema import TaskCreate, TaskUpdate

from app.models.user import User
from app.models.task_model import Task
import uuid



async def create_new_task(user: User, body: TaskCreate, db: AsyncSession):

    #smtm = insert(Task).values(**body.model_dump(exclude={"user_id"}), user_id=user.id).returning(Task)
    
    task = Task(**body.model_dump(exclude={"user_id"}), user_id=user.id)
    
    newTask = await task.save(db=db)

    return newTask



async def get_tasks(user: User, db: AsyncSession):
    
    tasks = await Task.find_by_user(db=db, user=user)

    return tasks



async def get_task_by_id(user: User, task_id: uuid.UUID, db: AsyncSession):

    #query = select(Task).options(selectinload(Task.user)).where(Task.id == task_id).where(Task.user_id == user.id)

    query = select(Task).where(and_(Task.id == task_id, Task.user_id == user.id))
    
    result = await db.execute(query)

    task = result.scalars().first()

    return task



async def get_all_tasks_and_their_user(db: AsyncSession):

    query = select(Task).options(selectinload(Task.user).load_only(User.email))

    result = await db.execute(query)

    tasks = result.scalars().all()

    return tasks



async def update_task(user: User, body: TaskUpdate, task_id: uuid.UUID, db: AsyncSession):

    updated_task = update(Task).where(and_(Task.id == task_id, Task.user_id == user.id)).values(title=body.title, description=body.description).returning(Task)

    result = await db.execute(updated_task)
        
    updated_tAsk = result.fetchone() 

    await db.commit()


    #if res:
    #    updated_task_dict = {column.name: getattr(res, column.name) for column in Task.__table__.columns}
    
    return updated_tAsk
    


async def update_task_orm_mode(user: User, body: TaskUpdate, task_id: uuid.UUID, db: AsyncSession):
    
    get_updated_task = select(Task).filter_by(id=task_id, user_id=user.id)

    result = await db.execute(get_updated_task)

    updated_task = result.scalar_one_or_none()

    if updated_task:

        updated_task.title = body.title

        updated_task.description = body.description

        await db.commit()

        await db.refresh(updated_task)

    return updated_task    



async def delete_task(user: User, task_id: uuid.UUID, db: AsyncSession):

    await db.execute(delete(Task).where(and_(Task.id == task_id, Task.user_id == user.id)))

    await db.commit()









    
