from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Transactions:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            transaction_id = db_app.transactions.insert_one(form.dict()).inserted_id
            db_app.transactions.update_one({'_id': ObjectId(transaction_id)}, {'$set': {
                'business_id': ObjectId(business_id),
                'payment_id': ObjectId(form['payment_id']),
                'invoice_id': ObjectId(form['invoice_id'])
            }})
            return form.dict()
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the transaction.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.transactions.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            return {"message": "We can't find any transactions. Its seems look empty"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, transaction_id: str) -> dict:
        try:
            transaction = db_app.transactions.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(transaction_id)})
            
            transaction['_id'] = str(transaction['_id'])
            transaction['business_id'] = str(transaction['business_id'])
            transaction['payment_id'] = str(transaction['payment_id'])
            transaction['invoice_id'] = str(transaction['invoice_id'])
            
            json_str = json_util.dumps(transaction)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="This Transaction ID is not exist!",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, transaction_id: str, form: dict) -> dict:
        try:
            db_app.transactions.update_one({'business_id': ObjectId(business_id), '_id': ObjectId(transaction_id)}, {'$set': form.dict()})
            return Transactions.find_one(business_id, transaction_id)

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the transaction.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, transaction_id: str) -> dict:
        try:
            db_app.transactions.delete_one({'_id': ObjectId(transaction_id), 'business_id': ObjectId(business_id)})
            return {"message": "Transaction was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="This Transaction ID is not exist!",
                headers={"WWW-Authenticate": "Bearer"},
            )
