from bson import ObjectId
from config.db.connection import db_app
from fastapi import HTTPException, status

class Tasks_log:
    
    def create_one(business_id: str) -> dict:
        try:
            tasks_log_id = db_app.tasks_log.insert_one({
                'tasks': []
            }).inserted_id
            db_app.business.update_one({'_id': ObjectId(business_id)}, {'$set': {
                'tasks_log_id': ObjectId(tasks_log_id)
            }})
            return {"message": f"A new Tasks Log has been created with id ${tasks_log_id}"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the tasks log.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def find_one(tasks_log_id: str) -> dict:
        try:
            tasks_log = db_app.tasks_log.find_one({'_id': ObjectId(tasks_log_id)})
            tasks_log['_id'] = str(tasks_log['_id'])
            return tasks_log
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Not exist any tasks log with this id!",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def push_one(tasks_log_id: str, form: dict) -> dict:
        try:
            db_app.tasks_log.update_one({'_id': ObjectId(tasks_log_id)}, {'$push': {'tasks': form.dict()}})
            return Tasks_log.find_one(tasks_log_id)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the tasks log.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(tasks_log_id: str) -> dict:
        try:
            db_app.tasks_log.delete_one({'_id': ObjectId(tasks_log_id)})
            return {"message": "Tasks log was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this tasks log id. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )

