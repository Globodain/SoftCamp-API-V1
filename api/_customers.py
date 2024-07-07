from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Customers:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            customer_id = db_app.customers.insert_one(form.dict()).inserted_id
            db_app.customers.update_one({'_id': ObjectId(customer_id)}, {'$set': {
                'business_id': ObjectId(business_id)
            }})
            return form.dict()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the customer.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.customers.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            return {"message": "We can't find any customer associated to this business id"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, customer_id: str) -> dict:
        try:
            customer = db_app.customers.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(customer_id)})
            
            if customer is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this customer id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            customer['_id'] = str(customer['_id'])
            customer['business_id'] = str(customer['business_id'])
            
            json_str = json_util.dumps(customer)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this customer id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, customer_id: str, form: dict) -> dict:
        try:
            db_app.customers.update_one({'business_id': ObjectId(business_id), '_id': customer_id}, {'$set': form.dict()})
            return Customers.find_one(business_id, customer_id)
 
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the customer.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, customer_id: str) -> dict:
        try:
            db_app.customers.delete_one({'_id': customer_id, 'business_id': ObjectId(business_id)})
            return {"message": "Customer was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this customer id. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
