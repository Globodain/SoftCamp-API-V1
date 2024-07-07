from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Payments:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            payment_id = db_app.payments.insert_one(form.dict()).inserted_id
            db_app.payments.update_one({'_id': ObjectId(payment_id)}, {'$set': {
                'business_id': ObjectId(business_id)
            }})
            return form.dict()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the payment.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.payments.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            return {"message": "We can't find any payments. Its seems look empty"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, payment_id: str) -> dict:
        try:
            payment = db_app.payments.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(payment_id)})
            
            if payment is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this payment id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            payment['_id'] = str(payment['_id'])
            payment['business_id'] = str(payment['business_id'])
            payment['customer_id'] = str(payment['customer_id'])
            payment['price_id'] = str(payment['price_id'])
            payment['transaction_id'] = str(payment['transaction_id'])
            
            json_str = json_util.dumps(payment)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this payment id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, payment_id: str, form: dict) -> dict:
        try:
            db_app.payments.update_one({'business_id': ObjectId(business_id), '_id': payment_id}, {'$set': form.dict()})
            return Payments.find_one(business_id, payment_id)

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the payment.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, payment_id: str) -> dict:
        try:
            db_app.payments.delete_one({'_id': payment_id, 'business_id': ObjectId(business_id)})
            return {"message": "Payment was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this payment id. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
