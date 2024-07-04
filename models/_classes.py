from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from models._subclasses import BusinessSubclass

class APIToken(BaseModel):
    access_token: str
    token_type: str

class APITokenData(BaseModel):
    username: Optional[str] = None

class FindAPIUser(BaseModel):
    _id: str
    username: str
    full_name: str
    email: str
    hashed_password: str = Field(None, exclude=True)
    disabled: bool = Field(None, exclude=True)
    softcamp_team: Optional[bool] = Field(None, exclude=True)
    
class CreateAPIUser(BaseModel):
    username: str
    full_name: str
    email: str
    password: str
    disabled: bool
    softcamp_team: Optional[bool]
    
class SuperAdmin(BaseModel):
    username: str
    password: str

### BUSINESS 

class CreateBusiness(BaseModel):
    _id: str

class GetBusinessModel(BaseModel):
    _id: str
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

class UpdateBusinessModel(BaseModel):
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

### USERS
class InviteUser(BaseModel):
    _id: str

class CreateUser(BaseModel):
    _id: str

class GetUsers(BaseModel):
    _id: str

class GetUser(BaseModel):
    _id: str

class UpdateUser(BaseModel):
    profile: BusinessSubclass.Profile

class DeleteUser(BaseModel):
    profile: BusinessSubclass.Profile

### ROLES
class CreateRole(BaseModel):
    _id: str

class GetRoles(BaseModel):
    _id: str

class GetRole(BaseModel):
    _id: str
    
class UpdateRole(BaseModel):
    _id: str
    
class DeleteRole(BaseModel):
    _id: str 

### BOOKINGS
class CreateBooking(BaseModel):
    _id: str

class GetBookings(BaseModel):
    _id: str

class GetBooking(BaseModel):
    _id: str
    
class UpdateBooking(BaseModel):
    _id: str

class AddAccommodation(BaseModel):
    _id: str

class DeleteBooking(BaseModel):
    _id: str 

### CUSTOMERS
class CreateCustomer(BaseModel):
    _id: str

class GetCustomers(BaseModel):
    _id: str

class GetCustomer(BaseModel):
    _id: str
    
class UpdateCustomer(BaseModel):
    _id: str
    
class DeleteCustomer(BaseModel):
    _id: str 

### TRANSACTIONS
class CreateTransaction(BaseModel):
    _id: str

class GetTransactions(BaseModel):
    _id: str

class GetTransaction(BaseModel):
    _id: str
    
class UpdateTransaction(BaseModel):
    _id: str
    
class DeleteTransaction(BaseModel):
    _id: str 
    
### INVOICES
class CreateInvoice(BaseModel):
    _id: str

class GetInvoices(BaseModel):
    _id: str

class GetInvoice(BaseModel):
    _id: str
    
class UpdateInvoice(BaseModel):
    _id: str
    
class DeleteInvoice(BaseModel):
    _id: str 

### PAYMENTS
class CreatePayment(BaseModel):
    _id: str
    
class GetPayments(BaseModel):
    _id: str
    
class GetPayment(BaseModel):
    _id: str
    
class UpdatePayment(BaseModel):
    _id: str
    
class DeletePayment(BaseModel):
    _id: str 


### PRICES
class CreatePrice(BaseModel):
    _id: str

class GetPrices(BaseModel):
    _id: str
    
class GetPrice(BaseModel):
    _id: str
    
class UpdatePrice(BaseModel):
    _id: str
    
class DeletePrice(BaseModel):
    _id: str 


### DISCOUNTS
class CreateDiscount(BaseModel):
    _id: str

class GetDiscounts(BaseModel):
    _id: str

class GetDiscount(BaseModel):
    _id: str
    
class UpdateDiscount(BaseModel):
    _id: str
    
class DeleteDiscount(BaseModel):
    _id: str 


### BANKS
class CreateBank(BaseModel):
    _id: str
    
class GetBanks(BaseModel):
    _id: str
    
class GetBank(BaseModel):
    _id: str
    
class UpdateBank(BaseModel):
    _id: str
    
class DeleteBank(BaseModel):
    _id: str 


### SERVICES
class CreateService(BaseModel):
    _id: str
    
class GetServices(BaseModel):
    _id: str

class GetService(BaseModel):
    _id: str
    
class UpdateService(BaseModel):
    _id: str
    
class DeleteService(BaseModel):
    _id: str 


### PERSONS
class CreatePerson(BaseModel):
    _id: str
    
class GetPersons(BaseModel):
    _id: str
    
class GetPerson(BaseModel):
    _id: str
    
class UpdatePerson(BaseModel):
    _id: str
    
class DeletePerson(BaseModel):
    _id: str 