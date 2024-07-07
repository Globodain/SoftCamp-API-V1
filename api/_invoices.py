from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Invoices:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            invoice_id = db_app.invoices.insert_one(form.dict()).inserted_id
            db_app.invoices.update_one({'_id': ObjectId(invoice_id)}, {'$set': {
                'business_id': ObjectId(business_id)
            }})
            return form.dict()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the invoice.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.invoices.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            return {"message": "We can't find any invoices. Its seems look empty"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, invoice_id: str) -> dict:
        try:
            invoice = db_app.invoices.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(invoice_id)})
            
            if invoice is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this invoice id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            invoice['_id'] = str(invoice['_id'])
            invoice['business_id'] = str(invoice['business_id'])
            invoice['payment_id'] = str(invoice['payment_id'])
            invoice['customer_id'] = str(invoice['customer_id'])
            
            json_str = json_util.dumps(invoice)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this invoice id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, invoice_id: str, form: dict) -> dict:
        try:
            db_app.invoices.update_one({'business_id': ObjectId(business_id), '_id': invoice_id}, {'$set': form.dict()})
            return Invoices.find_one(business_id, invoice_id)

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the invoice.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, invoice_id: str) -> dict:
        try:
            db_app.invoices.delete_one({'_id': invoice_id, 'business_id': ObjectId(business_id)})
            return {"message": "Invoice was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this invoice id. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
