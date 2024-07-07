from config.db.connection import db_app
from bson import ObjectId
from datetime import datetime,timedelta
from fastapi import HTTPException, status

from functions import Functions

class Invitations:
    
    def list_all(business_id: str) -> dict:
        response = []
        
        query = db_app.uid.find({'business_id': ObjectId(business_id)})

        if query is None:
            return {"message": "We can't find any invitations. Its seems look empty"}

        for i in query:
            i['_id'] = str(i['_id'])
            i['business_id'] = str(i['business_id'])
            i['expire'] = i['expire'].isoformat()
            response.append(i)
            
        return response

    def create(business_id: str, email: str) -> dict:
        salt = Functions.Generates.salt(16)
        serializer = Functions.Serializer.URLSafeTimed()
        uid = serializer.dumps(email, salt=salt)
        
        try:
            existing_entry = db_app.uid.find_one({
                'email': email, 
                'business_id': ObjectId(business_id)
            })
            
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business_id format incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        expiration = datetime.now() + timedelta(days=3)
        
        if existing_entry is None:
            db_app.uid.insert_one({
                '_uid': uid, 
                'business_id': ObjectId(business_id),
                'email': email, 
                'expire': expiration,
            })
        else:
            return {'status': 'error', 'message': 'An invitation has already been sent to this email'}
        
        return {'status': 'success', "message": "Invitation was send successfully"}
    
    def delete(business_id: str, email: str) -> dict:
        try:
            db_app.uid.delete_one({'email': str(email)})
            return {'status': "success", 'msg': f"Invitation to {email} was deleted"}
        
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find any invitation from this email",
                headers={"WWW-Authenticate": "Bearer"},
            )        
    def process_invitation(business_id: str, uid: str) -> dict:
        try:
            uid_data = db_app.uid.find_one({'business_id': ObjectId(business_id), '_uid': uid})
            db_app.uid.delete_one({'business_id': ObjectId(business_id), '_uid': uid})
        
            if datetime.now() > uid_data['expire']:
                raise HTTPException(
                    status_code=status.HTTP_408_REQUEST_TIMEOUT,
                    detail="Your invitation is expired!",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return {'status': "success", 'msg': f"The invitation was validated!. You can create now your user", 
                    'business_id': str(uid_data['business_id'])}
            
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="We can't find any invitation with this uid",
                headers={"WWW-Authenticate": "Bearer"},
            )    