from bson import ObjectId
from config.db.connection import db_app
from fastapi import HTTPException, status

class Repository:
    
    class Business:
            
        def create(business_id: str) -> dict:
            try:
                db_app.business_folders.insert_one({
                    "business_id": ObjectId(business_id),
                    "folders": [],
                    "status": "active"
                })
                return {'message': "The business repository was created!"}
            
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while creating the repository.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        
        def create_folder(business_id: str, folder_name: str) -> dict:
            try:
                db_app.business_folders.update_one({"business_id": ObjectId(business_id)}, {"$push": {
                    "folders": folder_name
                }})
                return {'message': "The folder was created!"}
            
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while creating the folder.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        def find_one(business_id: str) -> dict:
            try:
                repository = db_app.business_folders.find_one({'business_id': ObjectId(business_id)})
                repository['business_id'] = str(repository['business_id'])
                return repository
            except Exception as e:
                print(e)
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="This repository is not exist!",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
        def update_one(business_id: str, form: dict) -> dict:
            try:
                db_app.business_folders.update_one({'business_id': ObjectId(business_id)}, {'$set': form.dict()})
                return Repository.Business.find_one(business_id)
            
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while updating the repository.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        def delete(business_id: str) -> dict:
            try:
                db_app.business_folders.delete_one({'business_id': ObjectId(business_id)})
                return {"message": "Repository was deleted successfully!"}
            
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this business id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )


    class User:
            
        def create(user_id: str) -> dict:
            try:
                db_app.users_folders.insert_one({
                    "user_id": ObjectId(user_id),
                    "folders": [],
                    "status": "active"
                })
                return {'message': "The user repository was created!"}
            
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while creating the repository.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        
        def create_folder(user_id: str, folder_name: str) -> dict:
            try:
                db_app.users_folders.update_one({"user_id": ObjectId(user_id)}, {"$push": {
                    "folders": folder_name
                }})
                return {'message': "The folder was created!"}
            
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while creating the folder.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        def find_one(user_id: str) -> dict:
            try:
                repository = db_app.users_folders.find_one({'user_id': ObjectId(user_id)})
                repository['user_id'] = str(repository['user_id'])
                return repository
            
            except Exception as e:
                print(e)
                raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="This repository is not exist!",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                
        def update_one(user_id: str, form: dict) -> dict:
            try:
                db_app.users_folders.update_one({'user_id': ObjectId(user_id)}, {'$set': form.dict()})
                return Repository.User.find_one(user_id)

            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while updating the repository.",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        def delete(user_id: str) -> dict:
            try:
                db_app.users_folders.delete_one({'user_id': ObjectId(user_id)})
                return {"message": "Repository was deleted successfully!"}
            
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="We can't find this user id. Check it and try again",
                    headers={"WWW-Authenticate": "Bearer"},
                )