from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Services:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            service_id = db_app.services.insert_one(form.dict()).inserted_id
            db_app.services.update_one({'_id': ObjectId(service_id)}, {'$set': {
                'business_id': ObjectId(business_id)
            }})
            return form.dict()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the service.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.services.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find any services associated to this business id",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, service_id: str) -> dict:
        try:
            service = db_app.services.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(service_id)})
                
            service['_id'] = str(service['_id'])
            service['business_id'] = str(service['business_id'])
            
            if 'price_id' in service:
                service['price_id'] = str(service['price_id'])
            
            json_str = json_util.dumps(service)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this Service ID. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, service_id: str, form: dict) -> dict:
        try:
            db_app.services.update_one({'business_id': ObjectId(business_id), '_id': service_id}, {'$set': form.dict()})
            return Services.find_one(business_id, service_id)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the service.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, service_id: str) -> dict:
        try:
            db_app.services.delete_one({'_id': service_id, 'business_id': ObjectId(business_id)})
            return {"message": "Service was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this Service ID. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
