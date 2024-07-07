from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

from api._repository import Repository
from api._tokens import Tokens


class Users:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            # Create User
            user_id = db_app.users.insert_one(form.dict()).inserted_id
            if user_id:
                db_app.users.update_one({'_id': ObjectId(user_id)}, {'$set': {
                    'business_id': ObjectId(business_id),
                    'role_id': ObjectId(form['role_id'])
                }})
                
                # Create User Repository
                Repository.User.create(user_id)
                
                # Create Access Token
                Tokens.create_one(user_id)
                
                return form.dict()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the user.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the user.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def find() -> dict:
        query = db_app.users.find()
        
        if query is None:
            return {"message": "We can't find any User. Its seems look empty"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)
    
    def find_by_business(business_id: str) -> dict:
        query = db_app.users.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            return {"message": "We can't find any User. Its seems look empty"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, user_id: str) -> dict:
        try:
            user = db_app.users.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(user_id)})
            
            user['_id'] = str(user['_id'])
            user['business_id'] = str(user['business_id'])
            user['role_id'] = str(user['role_id'])
            
            json_str = json_util.dumps(user)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this User ID. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )   
            
    def update_one(business_id: str, user_id: str, form: dict) -> dict:
        try:
            db_app.users.update_one({'business_id': ObjectId(business_id), '_id': ObjectId(user_id)}, {'$set': form.dict()})
            return Users.find_one(business_id, user_id)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the user.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, user_id: str) -> dict:
        try:
            db_app.users.delete_one({'_id': ObjectId(user_id), 'business_id': ObjectId(business_id)})
            return {"message": "User was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this User ID. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )   
