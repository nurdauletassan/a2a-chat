from datetime import datetime
from ..core.celery_app import celery_app
from ..database.session import SessionLocal
from ..database.models import TaskLog

@celery_app.task
def write_timestamp():
    """
    Write current timestamp to the database.
    This task runs daily at midnight.
    """
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create database session
        db = SessionLocal()
        
        # Create task log entry
        task_log = TaskLog(
            task_name="daily_timestamp",
            status="success",
            message=f"Timestamp: {timestamp}"
        )
        
        # Save to database
        db.add(task_log)
        db.commit()
        
        return f"Timestamp written to database: {timestamp}"
        
    except Exception as e:
        # Log error to database if possible
        try:
            db = SessionLocal()
            error_log = TaskLog(
                task_name="daily_timestamp",
                status="error",
                message=f"Error writing timestamp: {str(e)}"
            )
            db.add(error_log)
            db.commit()
        except:
            pass
        
        return f"Error writing timestamp to database: {str(e)}"
    finally:
        db.close() 