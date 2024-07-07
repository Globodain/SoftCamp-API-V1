from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Discounts:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            discount_id = db_app.discounts.insert_one(form.dict()).inserted_id
            db_app.discounts.update_one({'_id': ObjectId(discount_id)}, {'$set': {
                'business_id': ObjectId(business_id)
            }})
            return form.dict()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the discount.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.discounts.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            return {"message": "We can't find any discount associated to this business id"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, discount_id: str) -> dict:
        try:
            discount = db_app.discounts.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(discount_id)})
            
            if discount is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this discount id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            discount['_id'] = str(discount['_id'])
            discount['business_id'] = str(discount['business_id'])
            
            json_str = json_util.dumps(discount)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this discount id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, discount_id: str, form: dict) -> dict:
        try:
            db_app.discounts.update_one({'business_id': ObjectId(business_id), '_id': discount_id}, {'$set': form.dict()})
            return Discounts.find_one(business_id, discount_id)

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the discount.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, discount_id: str) -> dict:
        try:
            db_app.discounts.delete_one({'_id': discount_id, 'business_id': ObjectId(business_id)})
            return {"message": "Discount was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this discount id. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
