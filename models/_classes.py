from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from models._subclasses import BusinessSubclass, UserSubclass, TasksSubclass, RepositorySubclass

class API:
        
    class APIToken(BaseModel):
        access_token: str
        token_type: str

    class APITokenData(BaseModel):
        email: Optional[str] = None

    class FindAPIUser(BaseModel):
        _id: str
        email: str
        full_name: str
        hashed_password: str = Field(None, exclude=True)
        disabled: bool = Field(None, exclude=True)
        softcamp_team: Optional[bool] = Field(None, exclude=True)

    class SuperAdmin(BaseModel):
        email: str
        password: str


    class CreateAPIUser(BaseModel):
        email: str
        full_name: str
        password: str
        disabled: bool
        softcamp_team: Optional[bool]
        testing: bool
        


class Business:
    class Create(BaseModel):
        _id: str

    class Get(BaseModel):
        _id: Optional[str]
        profile: BusinessSubclass.Profile
        business: BusinessSubclass.Information
        camping: BusinessSubclass.Camping
        stripe: BusinessSubclass.Stripe
        subscription: BusinessSubclass.Subscription
        martina: BusinessSubclass.Martina
        status: str
        task_log_id: str
        installed_modules: List[str]
        onboarding: bool
        settings: List[str]
        updated: datetime
        created: datetime # ObjectId().generation_time --> Para acceder a la fecha y hora de creacion del documento en datetime (UTC)

    class Update(BaseModel):
        profile: BusinessSubclass.Profile
        business: BusinessSubclass.Information
        camping: BusinessSubclass.Camping
        stripe: BusinessSubclass.Stripe
        subscription: BusinessSubclass.Subscription
        martina: BusinessSubclass.Martina
        status: str
        installed_modules: List[str]
        onboarding: bool
        settings: List[str]
        updated: datetime

    class Delete(BaseModel):
        business_id: str = Field(...,alias="_id")


class Invitations:
    class Get(BaseModel):
        invitation_id: str = Field(...,alias="_id")
    class Send(BaseModel):
        business_id: str = Field(None, exclude=True)
        email: str

    class Delete(BaseModel):
        business_id: str = Field(None, exclude=True)
        email: str

    class Process(BaseModel):
        _uid: str
        business_id: str = Field(None, exclude=True)


class Users:
        
    class Create(BaseModel):
        _id: str
        role_id: str
        business_id: str = Field(None, exclude=True)
        email: str
        secret_code: str
        personal: UserSubclass.Personal
        access: bool = True
        status: str = "active"
        toc: str = "accepted"
        
        
    class Get(BaseModel):
        _id: str
        business_id: str
        role_id: str
        email: str
        secret_code: str = Field(None, exclude=True)
        personal: UserSubclass.Personal
        emails: UserSubclass.Emails
        toc: str
        access: bool
        status: str
        updated: datetime

    class Update(BaseModel):
        email: str
        secret_code: str = Field(None, exclude=True)
        personal: UserSubclass.Personal
        emails: UserSubclass.Emails
        access: bool
        status: str

    class Delete(BaseModel):
        _id: str
        user_id: str
        business_id: str


class Roles:
        
    class Create(BaseModel):
        _id: str
        business_id: str 
        type: str
        permissions: dict

    class Get(BaseModel):
        role_id: str = Field(...,alias="_id")
        business_id: str = Field(None, exclude=True)
        type: str
        permissions: dict
        
    class Update(BaseModel):
        _id: str
        business_id: str = Field(None, exclude=True)
        type: str
        permissions: dict
        
    class Delete(BaseModel):
        _id: str 
        business_id: str


class Bookings:
    class Create(BaseModel):
        _id: str
    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str

    class AddAccommodation(BaseModel):
        _id: str

    class Delete(BaseModel):
        _id: str 


class Customers:
        
    class Create(BaseModel):
        _id: str
    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str
        
    class Delete(BaseModel):
        _id: str 


class Transactions:
        
    class Create(BaseModel):
        _id: str
    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str
        
    class Delete(BaseModel):
        _id: str 
        

class Invoices:
        
    class Create(BaseModel):
        _id: str

    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str
        
    class Delete(BaseModel):
        _id: str 


class Payments:
        
    class Create(BaseModel):
        _id: str
        
    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str
        
    class Delete(BaseModel):
        _id: str 



class Prices:
        
    class Create(BaseModel):
        _id: str
    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str
        
    class Delete(BaseModel):
        _id: str 


class Discounts:
        
    class Create(BaseModel):
        _id: str

    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str
        
    class Delete(BaseModel):
        _id: str 



class Banks:
        
    class Create(BaseModel):
        _id: str
        
    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str
        
    class Delete(BaseModel):
        _id: str 



class Services:
        
    class Create(BaseModel):
        _id: str

    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str
        
    class Delete(BaseModel):
        _id: str 



class Persons:
        
    class Create(BaseModel):
        _id: str
    class Get(BaseModel):
        _id: str
        
    class Update(BaseModel):
        _id: str
        
    class Delete(BaseModel):
        _id: str 
    

class TasksLog:
        
    class CreateRequestModel(BaseModel):
        business_id: str
        
    class CreateResponseModel(BaseModel):
        message: str
        
    class GetRequestModel(BaseModel):
        tasks_log_id: str = Field(...,alias="_id")
        tasks: List[TasksSubclass.Task]
        
    class GetResponseModel(BaseModel):
        tasks_log_id: str = Field(...,alias="_id")
        tasks: List[TasksSubclass.Task]
        
    class PushTaskRequestModel(BaseModel):
        title: str
        msg: str
        code: int
        status: str
        
    class PushTaskResponseModel(BaseModel):
        title: str
        msg: str
        code: int
        status: str
        
    class DeleteRequestModel(BaseModel):
        tasks_log_id: str = Field(...,alias="_id")

    class DeleteResponseModel(BaseModel):
        tasks_log_id: str = Field(...,alias="_id")

class Tokens:
    
    class CreateRequestModel(BaseModel):
        user_id: str
    
    class CreateResponseModel(BaseModel):
        token: str
    
    class GetRequestModel(BaseModel):
        user_id: str

    class GetResponseModel(BaseModel):
        token_id: str = Field(..., alias="_token")
        user_id: str
        last: str = Field(..., alias="_last")
        created: str
        
    class DeleteRequestModel(BaseModel):
        user_id: str
    
    class DeleteResponseModel(BaseModel):
        message: str
    
class Repository:
    class CreateBusinessRequestModel(BaseModel):
        business_id: str

    class CreateBusinessResponseModel(BaseModel):
        business_id: str

    class CreateUserRequestModel(BaseModel):
        user_id: str
        
    class CreateUserResponseModel(BaseModel):
        user_id: str
        
    class GetBusinessRequestModel(BaseModel):
        business_id: str
        
    class GetBusinessResponseModel(BaseModel):
        business_id: str
        

    class GetUserRequestModel(BaseModel):
        user_id: str

    class GetUserResponseModel(BaseModel):
        user_id: str

    class CreateFolderRequestModel(BaseModel):
        title: str
        description: str
        color: str
        status: str

    class CreateFolderResponseModel(BaseModel):
        title: str
        description: str
        color: str
        status: str


    class UploadFileRequestModel(BaseModel):
        filename: str
        
    class UploadFileResponseModel(BaseModel):
        filename: str
        
    class DeleteFolderRequestModel(BaseModel):
        folder_name: str
                
    class DeleteFolderResponseModel(BaseModel):
        folder_name: str

    class DeleteFileRequestModel(BaseModel):
        filename: str

    class DeleteFileResponseModel(BaseModel):
        filename: str

    class DeleteBusinessRequestModel(BaseModel):
        business_id: str
        
    class DeleteBusinessResponseModel(BaseModel):
        message: str

    class DeleteUserRequestModel(BaseModel):
        user_id: str
        
    class DeleteUserResponseModel(BaseModel):
        message: str