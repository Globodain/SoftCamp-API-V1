from bson import ObjectId,json_util
from config.db.connection import db_app,instance
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
import json
from api._tasks_log import Tasks_log
from api._repository import Repository
from libraries import Libraries

class Business:
    
    def create_one(business_id: str, form: dict) -> dict:
        try:
            business_id = db_app.business.insert_one(form.dict()).inserted_id

            # Create task log and assign to business
            Tasks_log.create_one(business_id)
            
            # Create business repository and assign to business
            Repository.Business.create(business_id)
            
            return form.dict()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the role.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def find() -> dict:
        query = db_app.business.find()
        
        if query is None:
            return {"message": "There're no businesses"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    def find_one(business_id: str) -> dict:
        try:
            business = db_app.business.find_one({'_id': ObjectId(business_id)})
        
            if business is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this Business ID. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            business['_id'] = str(business['_id'])
            business['task_log_id'] = str(business['task_log_id'])
            
            json_str = json_util.dumps(business)
            data = json.loads(json_str)
            return JSONResponse(content=data)
            
        except Exception as e:
            print(e)
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="This business id is not exist!",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
    def update_one(business_id: str, form: dict) -> dict:
        try:
            db_app.business.update_one({'_id': ObjectId(business_id)}, {'$set': form.dict()})
            return Business.find_one(business_id)
            
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the business.",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def delete_one(business_id: str) -> dict:
        # ONLY ITS POSSIBLE ON TEST MODE
        if instance != 'deployment':
            try:
                # Remove every document data with business assigned
                for user in db_app.users.find({'business_id': ObjectId(business_id)}):
                    db_app.users_folders.delete_one({'user_id': ObjectId(user['_id'])})
                    db_app.tokens.delete_one({'user_id': ObjectId(user['_id'])})
                db_app.users.delete_many({'business_id': ObjectId(business_id)})
                
                db_app.uid.delete_many({'business_id': ObjectId(business_id)})
                db_app.services.delete_many({'business_id': ObjectId(business_id)})
                db_app.roles.delete_many({'business_id': ObjectId(business_id)})
                db_app.prices.delete_many({'business_id': ObjectId(business_id)})
                db_app.persons.delete_many({'business_id': ObjectId(business_id)})
                db_app.payments.delete_many({'business_id': ObjectId(business_id)})
                db_app.customers.delete_many({'business_id': ObjectId(business_id)})
                db_app.bookings.delete_many({'business_id': ObjectId(business_id)})
                db_app.billings.delete_many({'business_id': ObjectId(business_id)})
                db_app.banks.delete_many({'business_id': ObjectId(business_id)})
                
                business = db_app.business.find_one({'_id': ObjectId(business_id)}, 
                                {'tasks_log_id': 1, 'stripe': 1})
                
                db_app.tasks_log.delete_one({'_id': ObjectId(business['tasks_log_id'])})
                db_app.onboardings.delete_one({'business_id': ObjectId(business_id)})
                db_app.business_folders.delete_many({'business_id': ObjectId(business_id)})
                
                # Remove data from Stripe
                Libraries.Stripe.Customers.delete_one(business['stripe']['customer'])
                Libraries.Stripe.ConnectedAccounts.delete_one(business['stripe']['account'], reason="fraud")
                
                # Remove data from Google Cloud
                Libraries.GoogleCloud.Functions.delete_folder(False, instance, business_id)
                
                db_app.business.delete_one({'_id': ObjectId(business_id)})
                return {"message": "Business was deleted successfully!"}
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="We can't find this business id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You can't delete real data on DB. Contact with SoftCamp support",
                headers={"WWW-Authenticate": "Bearer"},
            )
