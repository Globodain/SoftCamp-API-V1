from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Prices:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            price_id = db_app.prices.insert_one(form.dict()).inserted_id
            db_app.prices.update_one({'_id': ObjectId(price_id)}, {'$set': {
                'business_id': ObjectId(business_id)
            }})
            return form.dict()
    
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the price.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.prices.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            return {"message": "We can't find any prices. Its seems look empty"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, price_id: str) -> dict:
        try:
            price = db_app.prices.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(price_id)})
            
            if price is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this price id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
            price['_id'] = str(price['_id'])
            price['business_id'] = str(price['business_id'])
            
            if 'service_id' in price:
                price['service_id'] = str(price['service_id'])
            
            json_str = json_util.dumps(price)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this price id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, price_id: str, form: dict) -> dict:
        try:
            db_app.prices.update_one({'business_id': ObjectId(business_id), '_id': price_id}, {'$set': form.dict()})
            return Prices.find_one(business_id, price_id)
            
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the price.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, price_id: str) -> dict:
        try:
            db_app.prices.delete_one({'_id': price_id, 'business_id': ObjectId(business_id)})
            return {"message": "Price was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this price id. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
