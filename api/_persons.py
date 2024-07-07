from bson import ObjectId,json_util
from config.db.connection import db_app
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json

class Persons:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            person_id = db_app.persons.insert_one(form.dict()).inserted_id
            db_app.persons.update_one({'_id': ObjectId(person_id)}, {'$set': {
                'business_id': ObjectId(business_id)
            }})
            return form.dict()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the person.",
                headers={"WWW-Authenticate": "Bearer"},
            )


    def find(business_id: str) -> dict:
        query = db_app.persons.find({'business_id': ObjectId(business_id)})
        
        if query is None:
            return {"message": "We can't find any persons. Its seems look empty"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str, person_id: str) -> dict:
        try:
            # In this function, person_id is a str defined by Stripe
            person = db_app.persons.find_one({'business_id': ObjectId(business_id), '_id': ObjectId(person_id)})
            
            if person is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this person id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
                
            person['business_id'] = str(person['business_id'])
            
            json_str = json_util.dumps(person)
            data = json.loads(json_str)
            return JSONResponse(content=data)
        
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this person id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, person_id: str, form: dict) -> dict:
        try:
            db_app.persons.update_one({'business_id': ObjectId(business_id), '_id': person_id}, {'$set': form.dict()})
            return Persons.find_one(business_id, person_id)

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the person.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str, person_id: str) -> dict:
        try:
            db_app.persons.delete_one({'_id': person_id, 'business_id': ObjectId(business_id)})
            return {"message": "Person was deleted successfully!"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find this person id. Check it and try again",
                headers={"WWW-Authenticate": "Bearer"},
            )
