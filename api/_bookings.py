from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Bookings:
    
    def create_one(business_id: str, customer_id: str, payment_id: str, form: dict) -> dict:
        try:
            booking_id = db_app.bookings.insert_one(form.dict()).inserted_id
            
            # Every booking has got assigned a unique payment
            db_app.bookings.update_one({'_id': ObjectId(booking_id)}, {'$set': {
                'business_id': ObjectId(business_id),
                'customer_id': ObjectId(customer_id),
                'payment_id': ObjectId(payment_id)
            }})
            return form.dict()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the booking.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.bookings.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find any bookings associated to this Business ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_by_customer_id(business_id: str, customer_id: str) -> dict:
        query = db_app.bookings.find({'business_id': ObjectId(business_id), 'customer_id': ObjectId(customer_id)})
        
        if query is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find any bookings associated to this Customer ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_by_payment_id(business_id: str, payment_id: str) -> dict:
        query = db_app.bookings.find({'business_id': ObjectId(business_id), 'payment_id': ObjectId(payment_id)})
        
        if query is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find any bookings associated to this Payment ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, booking_id: str) -> dict:
        try:
            booking = db_app.bookings.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(booking_id)})
                
            booking['_id'] = str(booking['_id'])
            booking['business_id'] = str(booking['business_id'])
            booking['customer_id'] = str(booking['customer_id'])
            booking['payment_id'] = str(booking['payment_id'])
            
            json_str = json_util.dumps(booking)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this Booking ID. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, booking_id: str, form: dict) -> dict:
        try:
            db_app.bookings.update_one({'business_id': ObjectId(business_id), '_id': booking_id}, {'$set': form.dict()})
            return Bookings.find_one(business_id, booking_id)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the booking.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, booking_id: str) -> dict:
        try:
            db_app.bookings.delete_one({'_id': booking_id, 'business_id': ObjectId(booking_id)})
            return {"message": "Booking was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this Booking ID. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
