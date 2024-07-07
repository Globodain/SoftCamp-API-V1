from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Roles:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            role_id = db_app.roles.insert_one(form.dict()).inserted_id
            db_app.roles.update_one({'_id': ObjectId(role_id)}, {'$set': {
                'business_id': ObjectId(business_id)
            }})
            return form.dict()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the role.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.roles.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find any role associated to this business id",
                headers={"WWW-Authenticate": "Bearer"},
            )
                    
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, role_id: str) -> dict:
        try:
            role = db_app.roles.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(role_id)})
            role['_id'] = str(role['_id'])
            role['business_id'] = str(role['business_id'])
            return role
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this role id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, role_id: str, form: dict) -> dict:
        try:
            db_app.roles.update_one({'business_id': ObjectId(business_id), '_id': ObjectId(role_id)}, {'$set': form.dict()})
            return Roles.find_one(business_id, role_id)
            
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the role.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, role_id: str) -> dict:
        try:
            db_app.roles.delete_one({'_id': ObjectId(role_id), 'business_id': ObjectId(business_id)})
            return {"message": "Role was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this Role ID. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
