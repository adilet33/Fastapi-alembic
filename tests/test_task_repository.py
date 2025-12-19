import pytest
import uuid
from app.repository.task import (
    create_new_task,
    get_tasks,
    get_task_by_id,
    get_all_tasks_and_their_user,
    update_task,
    delete_task
)
from app.schemas.tasks_schema import TaskCreate, TaskUpdate
from app.models.task_model import Task


class TestTaskRepository:
    """Test task repository functions."""
    
    @pytest.mark.asyncio
    async def test_create_new_task(self, test_db, test_user):
        """Test creating a new task."""
        task_data = TaskCreate(
            title="Repository Test Task",
            description="Test description"
        )
        
        new_task = await create_new_task(
            user=test_user,
            body=task_data,
            db=test_db
        )
        
        assert new_task is not None
        assert new_task.title == "Repository Test Task"
        assert new_task.user_id == test_user.id
    
    @pytest.mark.asyncio
    async def test_get_tasks(self, test_db, test_user):
        """Test getting user's tasks."""
        # Create multiple tasks
        for i in range(3):
            task = Task(
                id=uuid.uuid4(),
                title=f"Task {i}",
                description=f"Description {i}",
                user_id=test_user.id
            )
            test_db.add(task)
        await test_db.commit()
        
        tasks = await get_tasks(user=test_user, db=test_db)
        
        assert len(tasks) == 3
    
    @pytest.mark.asyncio
    async def test_get_task_by_id(self, test_db, test_user, test_task):
        """Test getting task by ID."""
        task = await get_task_by_id(
            user=test_user,
            task_id=test_task.id,
            db=test_db
        )
        
        assert task is not None
        assert task.id == test_task.id
        assert task.title == test_task.title
    
    @pytest.mark.asyncio
    async def test_get_task_by_id_wrong_user(self, test_db, test_user2, test_task):
        """Test getting task with wrong user."""
        task = await get_task_by_id(
            user=test_user2,
            task_id=test_task.id,
            db=test_db
        )
        
        # Should return None as task belongs to different user
        assert task is None
    
    @pytest.mark.asyncio
    async def test_get_all_tasks_and_their_user(self, test_db, test_task):
        """Test getting all tasks with user info."""
        tasks = await get_all_tasks_and_their_user(db=test_db)
        
        assert len(tasks) > 0
        # Check that we can access user email
        for task in tasks:
            assert task.user is not None
    
    @pytest.mark.asyncio
    async def test_update_task(self, test_db, test_user, test_task):
        """Test updating a task."""
        update_data = TaskUpdate(
            title="Updated Title",
            description="Updated Description"
        )
        
        updated_task = await update_task(
            user=test_user,
            body=update_data,
            task_id=test_task.id,
            db=test_db
        )
        
        # The function returns a Row tuple from RETURNING clause
        assert updated_task is not None
    
    @pytest.mark.asyncio
    async def test_update_task_wrong_user(self, test_db, test_user2, test_task):
        """Test updating task with wrong user."""
        update_data = TaskUpdate(
            title="Should Not Update",
            description="Should Not Update"
        )
        
        updated_task = await update_task(
            user=test_user2,
            body=update_data,
            task_id=test_task.id,
            db=test_db
        )
        
        # Should return None as task belongs to different user
        assert updated_task is None
    
    @pytest.mark.asyncio
    async def test_delete_task(self, test_db, test_user):
        """Test deleting a task."""
        # Create a task to delete
        task = Task(
            id=uuid.uuid4(),
            title="To Delete",
            description="Will be deleted",
            user_id=test_user.id
        )
        test_db.add(task)
        await test_db.commit()
        task_id = task.id
        
        # Delete the task
        await delete_task(
            user=test_user,
            task_id=task_id,
            db=test_db
        )
        
        # Verify deletion
        deleted_task = await get_task_by_id(
            user=test_user,
            task_id=task_id,
            db=test_db
        )
        assert deleted_task is None
    
    @pytest.mark.asyncio
    async def test_delete_task_wrong_user(self, test_db, test_user, test_user2):
        """Test deleting task with wrong user."""
        # Create a task for user1
        task = Task(
            id=uuid.uuid4(),
            title="User1 Task",
            description="Belongs to user1",
            user_id=test_user.id
        )
        test_db.add(task)
        await test_db.commit()
        task_id = task.id
        
        # Try to delete with user2
        await delete_task(
            user=test_user2,
            task_id=task_id,
            db=test_db
        )
        
        # Task should still exist
        existing_task = await get_task_by_id(
            user=test_user,
            task_id=task_id,
            db=test_db
        )
        assert existing_task is not None
