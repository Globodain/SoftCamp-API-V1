from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Tokens:
    
    def create_one(user_id: str) -> dict:
        try:
            token_id = db_app.tokens.insert_one({
                'user_id': ObjectId(user_id)
            }).inserted_id
            return {'message': F'Access Token was created with Token ID {token_id}'}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the Access Token.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def find_one(user_id: str) -> dict:
        try:
            token = db_app.tokens.find_one({'user_id': ObjectId(user_id)})
            
            token['_id'] = str(token['_id'])
            token['user_id'] = str(token['user_id'])
            
            json_str = json_util.dumps(token)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this Access Token ID. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def delete_one(user_id: str) -> dict:
        try:
            db_app.tokens.delete_one({'user_id': ObjectId(user_id)})
            return {"message": "Access Token was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this Access Token ID. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
