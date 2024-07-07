from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Banks:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            bank_id = db_app.banks.insert_one(form.dict()).inserted_id
            if bank_id:
                db_app.banks.update_one({'_id': ObjectId(bank_id)}, {'$set': {
                    'business_id': ObjectId(business_id)
                }})
                return form.dict()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while registering the bank account.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while registering the bank account.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.banks.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find any bank account associated to this business id",
                headers={"WWW-Authenticate": "Bearer"},
            )        
            
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, bank_id: str) -> dict:
        try:
            # In this function, bank_id is a str defined by Stripe
            bank = db_app.banks.find_one({'business_id': ObjectId(business_id), '_id': bank_id})
            
            if bank is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this bank account. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            bank['business_id'] = str(bank['business_id'])
            
            json_str = json_util.dumps(bank)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this bank account. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, bank_id: str, form: dict) -> dict:
        try:
            if db_app.banks.update_one({'business_id': ObjectId(business_id), '_id': bank_id}, {'$set': form.dict()}):
                return Banks.find_one(business_id, bank_id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the bank account.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the bank account.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, bank_id: str) -> dict:
        try:
            db_app.banks.delete_one({'_id': bank_id, 'business_id': ObjectId(business_id)})
            return {"message": "Bank account was deleted successfully!"}
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this bank account. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
