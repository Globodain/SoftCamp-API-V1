from fastapi import APIRouter, Request, Depends, HTTPException, Form, status, Response, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth._control import oauth2_scheme,authenticate_user,get_password_hash,get_current_active_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,SUPERADMIN_PASSWORD,get_support_team
from config.db.connection import db_api
from datetime import timedelta
from typing import List

# Imports
from api import Functions
from public.examples import Examples
from models._classes import API as APIClass
from models._classes import Business as BusinessClass
from models._classes import Invitations as InvitationsClass
from models._classes import Users as UsersClass
from models._classes import Roles as RolesClass
from models._classes import Bookings as BookingsClass
from models._classes import Customers as CustomersClass
from models._classes import Transactions as TransactionsClass
from models._classes import Invoices as InvoicesClass
from models._classes import Payments as PaymentsClass
from models._classes import Prices as PricesClass
from models._classes import Discounts as DiscountsClass
from models._classes import Banks as BanksClass
from models._classes import Services as ServicesClass
from models._classes import Persons as PersonsClass
from models._classes import TasksLog as TasksLogClass
from models._classes import Tokens as TokensClass
from models._classes import Repository as RepositoryClass

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


class Knowledges:
    
    @router.get("/documentation/business", response_class=HTMLResponse,
    summary="Business",
    include_in_schema=False)
    def business(request: Request):
        return templates.TemplateResponse("sign-in.html", {"request": request})

class Authentication:
        
    invalid_tokens = set()
        
    @router.get("/my-account", tags=['API User'], response_model=APIClass.FindAPIUser)
    async def my_account(
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return current_user

    @router.get("/account", response_class=HTMLResponse,
    summary="Login",
    include_in_schema=False)
    def account(request: Request):
        return templates.TemplateResponse("sign-in.html", {"request": request})
    
    @router.get("/logout", response_class=HTMLResponse,
    summary="Logout",
    include_in_schema=False)
    def logout(response: Response, token: str = Depends(oauth2_scheme)):
        # Aquí invalidamos el token añadiéndolo al conjunto de tokens invalidados
        Authentication.invalid_tokens.add(token)
        response.delete_cookie(key="access_token")
        return RedirectResponse(url="/account")

    @router.post("/authentication", include_in_schema=False)
    async def login_for_access_token(response: Response, email: str = Form(...), password: str = Form(...)):
        user = authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user['email']}, expires_delta=access_token_expires
        )
        
        redirect_response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        redirect_response.set_cookie(
            "session",
            value=access_token,
            httponly=True,
            max_age=1800,
            expires=1800,
        )
        return redirect_response
    
    @router.post("/token", include_in_schema=False, response_model=APIClass.APIToken)
    def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user['email']}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

class Admin:
        
    @router.post("/add_user", include_in_schema=False)
    async def add_user(user: APIClass.CreateAPIUser, admin: APIClass.SuperAdmin):
        # Check if the provided password is correct
        if admin.password != SUPERADMIN_PASSWORD:
            raise HTTPException(status_code=400, detail="Incorrect superadmin password")

        # Check if the email already exists in the database
        if db_api.users.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already exists")

        # Hash the user's password
        hashed_password = get_password_hash(user.password)

        # Insert the new user into the database
        db_api.users.insert_one({
            "email": user.email,
            "full_name": user.full_name,
            "email": user.email,
            "email": user.email,
            "hashed_password": hashed_password,
            "disabled": user.disabled,
            "testing": True,
            "softcamp_team": user.softcamp_team
        })

        return {"message": "User added successfully"}

class ApiUsers:

    @router.get("/users", tags=["API User"], include_in_schema=False)
    async def get_users(current_user: dict = Depends(get_support_team)):
        user_list = list(db_api.users.find())
        for user in user_list:
            user["_id"] = str(user["_id"])
        return user_list

class Business:
    @router.post("/business", tags=["Business"])
    async def create_business(
        business: BusinessClass.Create = Body(..., example=Examples.Business.Create),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Business.create_one(business) 
    
    @router.get("/business", response_model=List[BusinessClass.Get], tags=["Business"])
    async def get_businesses(
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Business.find() 
    
    @router.get("/business/{business_id}", response_model=BusinessClass.Get, tags=["Business"])
    async def get_business(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Business.find_one(business_id) 

    @router.put("/business/{business_id}", response_model=BusinessClass.Update, tags=["Business"])
    async def update_business(
        business_id: str,
        business: BusinessClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Business.update_one(business_id, business)

    @router.delete("/business/{business_id}", response_model=BusinessClass.Delete, description="**Attention**: Delete one business will remove all data assigned.", tags=["Business"])
    async def delete_business(
        business_id: str,
        business: BusinessClass.Delete  = Body(..., example=Examples.Business.Delete),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Business.delete_one(business_id)

class Invitations:
    @router.get("/invitations/{business_id}", response_model=List[InvitationsClass.Get], tags=["Invitations"])
    async def see_all_invitations(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Invitations.list_all(business_id)

    @router.post("/invitations/{business_id}/{email}", response_model=InvitationsClass.Send, tags=["Invitations"])
    async def invite_user(
        business_id: str,
        email: str,
        invitations: InvitationsClass.Send = Body(..., example=Examples.Invitations.Create),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Invitations.create(business_id, email)
        
    @router.delete("/invitations/{business_id}/{email}", response_model=List[InvitationsClass.Delete], tags=["Invitations"])
    async def delete_invitation(
        business_id: str,
        email: str,
        invitations: InvitationsClass.Delete = Body(..., example=Examples.Invitations.Delete),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Invitations.delete(business_id, email)
        
    @router.post("/invitations/{business_id}/process/{uid}", response_model=InvitationsClass.Process, tags=["Invitations"])
    async def process_uid_from_invitation(
        business_id: str,
        uid: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Invitations.process_invitation(business_id, uid)
class Users:
    @router.post("/users/{business_id}", tags=["Users"])
    async def create_user(
        business_id: str, 
        form: UsersClass.Create, 
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Users.create_one(business_id, form)

    @router.get("/users/{business_id}", response_model=List[UsersClass.Get], tags=["Users"])
    async def get_users(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Users.find(business_id)
    
    @router.get("/users/{business_id}/{user_id}", response_model=UsersClass.Get, tags=["Users"])
    async def get_user(
        business_id: str,
        user_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Users.find_one(business_id, user_id)

    @router.put("/users/{business_id}/{user_id}", response_model=UsersClass.Update, tags=["Users"])
    async def update_user(
        business_id: str,
        user_id: str,
        user: UsersClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Users.update_one(business_id, user_id, user)
    
    @router.delete("/users/{business_id}/{user_id}", response_model=UsersClass.Delete, tags=["Users"])
    async def delete_user(
        business_id: str,
        user_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Users.delete_one(business_id, user_id)

class Roles:    
    @router.post("/roles/{business_id}", response_model=RolesClass.Create, tags=["Roles"])
    async def create_role(
        business_id: str,
        role: RolesClass.Create = Body(..., example=Examples.Roles.Create),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Roles.create_one(business_id) 
    
    @router.get("/roles/{business_id}", response_model=List[RolesClass.Get], tags=["Roles"])
    async def get_roles(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Roles.find(business_id) 
    
    @router.get("/roles/{business_id}/{role_id}", response_model=RolesClass.Get, tags=["Roles"])
    async def get_role(
        business_id: str,
        role_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Roles.find_one(business_id, role_id) 

    @router.put("/roles/{business_id}/{role_id}", response_model=RolesClass.Update, tags=["Roles"])
    async def update_role(
        business_id: str,
        role_id: str,
        role: RolesClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Roles.update_one(business_id, role_id, role) 

    @router.delete("/roles/{business_id}/{role_id}", response_model=RolesClass.Delete, tags=["Roles"])
    async def delete_role(
        business_id: str,
        role_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Roles.delete_one(business_id, role_id) 

class Bookings:    
    @router.post("/bookings/{business_id}", response_model=BookingsClass.Create, tags=["Bookings"])
    async def create_booking(
        business_id: str,
        booking: BookingsClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Bookings.create_one(business_id, booking) 
    
    @router.get("/bookings/{business_id}", response_model=List[BookingsClass.Get], tags=["Bookings"])
    async def get_bookings(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Bookings.find(business_id) 
    
    @router.get("/bookings/{business_id}/{booking_id}", response_model=BookingsClass.Get, tags=["Bookings"])
    async def get_booking(
        business_id: str,
        booking_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Bookings.find_one(business_id, booking_id) 

    @router.get("/bookings/{business_id}/{customer_id}", response_model=BookingsClass.Get, tags=["Bookings"])
    async def get_booking_by_customer(
        business_id: str,
        customer_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Bookings.find_by_customer_id(business_id, customer_id) 

    @router.get("/bookings/{business_id}/{payment_id}", response_model=BookingsClass.Get, tags=["Bookings"])
    async def get_booking_by_payment(
        business_id: str,
        payment_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Bookings.find_by_payment_id(business_id, payment_id) 

    @router.put("/bookings/{business_id}/{booking_id}", response_model=BookingsClass.Update, tags=["Bookings"])
    async def update_bookings(
        business_id: str,
        booking_id: str,
        booking: BookingsClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Bookings.update_one(business_id, booking_id, booking) 

    @router.put("/bookings/{business_id}/{booking_id}/{spot_id}", response_model=BookingsClass.AddAccommodation, tags=["Bookings"])
    async def add_other_accomodation_to_booking(
        business_id: str,
        booking_id: str,
        spot_id: str,
        booking: BookingsClass.AddAccommodation,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Bookings.add_accommodation(business_id, booking_id, spot_id, booking) 

    @router.delete("/bookings/{business_id}/{booking_id}", response_model=BookingsClass.Delete, tags=["Bookings"])
    async def delete_booking(
        business_id: str,
        booking_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Bookings.delete_one(business_id, booking_id) 

    
class Customers:
    @router.post("/customers/{business_id}", response_model=CustomersClass.Create, tags=["Customers"])
    async def create_customer(
        business_id: str,
        customer: CustomersClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Customers.create_one(business_id, customer) 
    
    @router.get("/customers/{business_id}", response_model=List[CustomersClass.Get], tags=["Customers"])
    async def get_customers(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Customers.find(business_id) 
    
    @router.get("/customers/{business_id}/{customer_id}", response_model=CustomersClass.Get, tags=["Customers"])
    async def get_customer(
        business_id: str,
        customer_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Customers.find_one(business_id, customer_id) 

    @router.put("/customers/{business_id}/{customer_id}", response_model=CustomersClass.Update, tags=["Customers"])
    async def update_customer(
        business_id: str,
        customer_id: str,
        customer: CustomersClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Customers.update_one(business_id, customer_id, customer) 

    @router.delete("/customers/{business_id}/{customer_id}", response_model=CustomersClass.Delete, tags=["Customers"])
    async def delete_customer(
        business_id: str,
        customer_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Customers.delete_one(business_id, customer_id) 
    
class Transactions:
    @router.post("/transactions/{business_id}", response_model=TransactionsClass.Create, tags=["Transactions"])
    async def create_transaction(
        business_id: str,
        transaction: TransactionsClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Transactions.create_one(business_id, transaction) 
    
    @router.get("/transactions/{business_id}", response_model=List[TransactionsClass.Get], tags=["Transactions"])
    async def get_transactions(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Transactions.find(business_id) 
    
    @router.get("/transactions/{business_id}/{transaction_id}", response_model=TransactionsClass.Get, tags=["Transactions"])
    async def get_transaction(
        business_id: str,
        transaction_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Transactions.find_one(business_id, transaction_id) 
    
    @router.put("/transactions/{business_id}/{transaction_id}", response_model=TransactionsClass.Update, tags=["Transactions"])
    async def update_transaction(
        business_id: str,
        transaction_id: str,
        transaction: TransactionsClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Transactions.update_one(business_id, transaction_id, transaction) 

    @router.delete("/transactions/{business_id}/{transaction_id}", response_model=TransactionsClass.Delete, tags=["Transactions"])
    async def delete_transaction(
        business_id: str,
        transaction_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Transactions.delete_one(business_id, transaction_id) 

 
class Invoices:    
    @router.post("/invoices/{business_id}", response_model=InvoicesClass.Create, tags=["Invoices"])
    async def create_invoice(
        business_id: str,
        invoice: InvoicesClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Invoices.create_one(business_id, invoice) 
    
    @router.get("/invoices/{business_id}", response_model=List[InvoicesClass.Get], tags=["Invoices"])
    async def get_invoices(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Invoices.find(business_id) 
    
    @router.get("/invoices/{business_id}/{invoice_id}", response_model=InvoicesClass.Get, tags=["Invoices"])
    async def get_invoice(
        business_id: str,
        invoice_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Invoices.find_one(business_id, invoice_id) 
    
    @router.put("/invoices/{business_id}/{invoice_id}", response_model=InvoicesClass.Update, tags=["Invoices"])
    async def update_invoice(
        business_id: str,
        invoice_id: str,
        invoice: InvoicesClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Invoices.update_one(business_id, invoice_id, invoice) 

    @router.delete("/invoices/{business_id}/{invoice_id}", response_model=InvoicesClass.Delete, tags=["Invoices"])
    async def delete_invoice(
        business_id: str,
        invoice_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Invoices.delete_one(business_id, invoice_id) 


class Payments:    
    @router.post("/payments/{business_id}", response_model=PaymentsClass.Create, tags=["Payments"])
    async def create_payment(
        business_id: str,
        payment: PaymentsClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Payments.create_one(business_id, payment) 
    
    @router.get("/payments/{business_id}", response_model=List[PaymentsClass.Get], tags=["Payments"])
    async def get_payments(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Payments.find(business_id) 
    
    @router.get("/payments/{business_id}/{payment_id}", response_model=PaymentsClass.Get, tags=["Payments"])
    async def get_payment(
        business_id: str,
        payment_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Payments.find_one(business_id, payment_id) 

    @router.put("/payments/{business_id}/{payment_id}", response_model=PaymentsClass.Update, tags=["Payments"])
    async def update_payment(
        business_id: str,
        payment_id: str,
        payment: PaymentsClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Payments.update_one(business_id, payment_id, payment) 

    @router.delete("/payments/{business_id}/{payment_id}", response_model=PaymentsClass.Delete, tags=["Payments"])
    async def delete_payment(
        business_id: str,
        payment_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Payments.delete_one(business_id, payment_id) 


class Prices:    
    @router.post("/prices/{business_id}", response_model=PricesClass.Create, tags=["Prices"])
    async def create_price(
        business_id: str,
        price: PricesClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Prices.create_one(business_id, price) 
    
    @router.get("/prices/{business_id}", response_model=List[PricesClass.Get], tags=["Prices"])
    async def get_prices(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Prices.find(business_id) 
    
    @router.get("/prices/{business_id}/{price_id}", response_model=PricesClass.Get, tags=["Prices"])
    async def get_price(
        business_id: str,
        price_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Prices.find_one(business_id, price_id) 

    @router.put("/prices/{business_id}/{price_id}", response_model=PricesClass.Update, tags=["Prices"])
    async def update_price(
        business_id: str,
        price_id: str,
        price: PricesClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Prices.update_one(business_id, price_id, price) 

    @router.delete("/prices/{business_id}/{price_id}", response_model=PricesClass.Delete, tags=["Prices"])
    async def delete_price(
        business_id: str,
        price_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Prices.delete_one(business_id, price_id) 


class Discounts:    
    @router.post("/discounts/{business_id}", response_model=DiscountsClass.Create, tags=["Discounts"])
    async def create_discount(
        business_id: str,
        discount: DiscountsClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Discounts.create_one(business_id, discount) 
    
    @router.get("/discounts/{business_id}", response_model=List[DiscountsClass.Get], tags=["Discounts"])
    async def get_discounts(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Discounts.find(business_id) 
    
    @router.get("/discounts/{business_id}/{discount_id}", response_model=DiscountsClass.Get, tags=["Discounts"])
    async def get_discount(
        business_id: str,
        discount_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Discounts.find_one(business_id, discount_id) 
    
    @router.put("/discounts/{business_id}/{discount_id}", response_model=DiscountsClass.Update, tags=["Discounts"])
    async def update_discounts(
        business_id: str,
        discount_id: str,
        discount: DiscountsClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Discounts.update_one(business_id, discount_id, discount) 

    @router.delete("/discounts/{business_id}/{discount_id}", response_model=DiscountsClass.Delete, tags=["Discounts"])
    async def delete_discount(
        business_id: str,
        discount_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Discounts.delete_one(business_id, discount_id) 


class Banks:    
    @router.post("/banks/{business_id}", response_model=BanksClass.Create, tags=["Banks"])
    async def create_bank(
        business_id: str,
        bank: BanksClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Banks.create_one(business_id, bank) 
    
    @router.get("/banks/{business_id}", response_model=List[BanksClass.Get], tags=["Banks"])
    async def get_banks(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Banks.find(business_id) 
    
    @router.get("/banks/{business_id}/{bank_id}", response_model=BanksClass.Get, tags=["Banks"])
    async def get_bank(
        business_id: str,
        bank_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Banks.find_one(business_id, bank_id) 

    @router.put("/banks/{business_id}/{bank_id}", response_model=BanksClass.Update, tags=["Banks"])
    async def update_bank(
        business_id: str,
        bank_id: str,
        bank: BanksClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Banks.update_one(business_id, bank_id, bank) 
    
    @router.delete("/banks/{business_id}/{bank_id}", response_model=BanksClass.Delete, tags=["Banks"])
    async def delete_bank(
        business_id: str,
        bank_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Banks.delete_one(business_id, bank_id) 


class Services:    
    @router.post("/services/{business_id}", response_model=ServicesClass.Create, tags=["Services"])
    async def create_service(
        business_id: str,
        service: ServicesClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Services.create_one(business_id, service) 
    
    @router.get("/services/{business_id}", response_model=List[ServicesClass.Get], tags=["Services"])
    async def get_services(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Services.find(business_id) 
    
    @router.get("/services/{business_id}/{service_id}", response_model=ServicesClass.Get, tags=["Services"])
    async def get_service(
        business_id: str,
        service_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Services.find_one(business_id, service_id) 

    @router.put("/services/{business_id}/{service_id}", response_model=ServicesClass.Update, tags=["Services"])
    async def update_service(
        business_id: str,
        service_id: str,
        service: ServicesClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Services.update_one(business_id, service_id, service) 

    @router.delete("/services/{business_id}/{service_id}", response_model=ServicesClass.Delete, tags=["Services"])
    async def delete_service(
        business_id: str,
        service_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Services.delete_one(business_id, service_id) 


class Persons:    
    @router.post("/persons/{business_id}", response_model=PersonsClass.Create, tags=["Persons"])
    async def create_person(
        business_id: str,
        person: PersonsClass.Create,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Persons.create_one(business_id, person) 
    
    @router.get("/persons/{business_id}", response_model=List[PersonsClass.Get], tags=["Persons"])
    async def get_persons(
        business_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Persons.find(business_id) 
    
    @router.get("/persons/{business_id}/{person_id}", response_model=PersonsClass.Get, tags=["Persons"])
    async def get_person(
        business_id: str,
        person_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Persons.find_one(business_id, person_id) 

    @router.put("/persons/{business_id}/{person_id}", response_model=PersonsClass.Update, tags=["Persons"])
    async def update_person(
        business_id: str,
        person_id: str,
        person: PersonsClass.Update,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Persons.update_one(business_id, person_id, person) 

    @router.delete("/persons/{business_id}/{person_id}", response_model=PersonsClass.Delete, tags=["Persons"])
    async def delete_person(
        business_id: str,
        person_id: str,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Persons.delete_one(business_id, person_id) 

class TasksLogs:    
    @router.post("/logs/tasks", response_model=TasksLogClass.CreateResponseModel, tags=["TasksLog"],
        description="**Important**: The Tasks log must be assigned to a business. This Tasks log is automatically created with the business log, but can be deleted (cleaned) and recreated.",
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.TasksLog.CreateResponse}}}}
    )
    async def create_tasks_log(
        business_id: str,
        tasks_log: TasksLogClass.CreateRequestModel = Body(..., example=Examples.TasksLog.CreateRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Tasks_log.create_one(tasks_log) 
    
    
    @router.get("/logs/tasks/{tasks_log_id}", response_model=List[TasksLogClass.GetResponseModel], tags=["TasksLog"],
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.TasksLog.GetResponse}}}}
    )
    async def get_tasks_log(
        tasks_log_id: str,
        tasks_log: TasksLogClass.GetRequestModel = Body(..., example=Examples.TasksLog.GetRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Tasks_log.find_one(tasks_log_id) 


    @router.put("/logs/tasks/{tasks_log_id}", response_model=TasksLogClass.PushTaskResponseModel, tags=["TasksLog"],
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.TasksLog.PushTaskResponse}}}}
    )
    async def push_task_to_log(
        tasks_log_id: str,
        task_data: TasksLogClass.PushTaskRequestModel = Body(..., example=Examples.TasksLog.PushTaskRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Tasks_log.push_one(tasks_log_id, task_data) 


    @router.delete("/logs/tasks/{tasks_log_id}", tags=["TasksLog"],
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.TasksLog.DeleteResponse}}}}
    )
    async def delete_tasks_log(
        tasks_log_id: str,
        tasks_log: TasksLogClass.DeleteRequestModel = Body(..., example=Examples.TasksLog.DeleteRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Tasks_log.delete_one(tasks_log_id) 


class Tokens:    
    @router.post("/tokens", response_model=TokensClass.CreateResponseModel, tags=["Tokens"],
        description="**Important**: The Access Token must be assigned to a User. This Access Token is automatically created when User is created, but can be deleted (cleaned) and recreated.",
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.Tokens.CreateResponse}}}}
    )
    async def create_access_token(
        user_id: str,
        tokens: TokensClass.CreateRequestModel,
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Tokens.create_one(user_id) 
    
    
    @router.get("/tokens/{user_id}", response_model=TokensClass.GetResponseModel, tags=["Tokens"],
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.Tokens.GetResponse}}}}
    )
    async def get_access_token(
        user_id: str,
        token: TokensClass.GetRequestModel = Body(..., example=Examples.Tokens.GetRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Tokens.find_one(user_id) 


    @router.delete("/tokens/{user_id}", response_model=TokensClass.DeleteResponseModel, tags=["Tokens"],
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.Tokens.DeleteResponse}}}}
    )
    async def delete_access_token(
        user_id: str,
        token: TokensClass.DeleteRequestModel = Body(..., example=Examples.Tokens.DeleteRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Tokens.delete_one(user_id) 


class Repository:
    
    @router.post("/repository/{business_id}", response_model=RepositoryClass.CreateBusinessRequestModel, tags=["Repository"],
        description="**Important**: The repository must be assigned to a business. This repository is automatically created with the business log, but can be deleted (cleaned) and recreated.",
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.Repository.CreateBusinessResponse}}}}
    )
    async def create_business_repository(
        business_id: str,
        repository: RepositoryClass.CreateBusinessRequestModel = Body(..., example=Examples.Repository.CreateBusinessRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Repository.Business.create(business_id) 
    
    
    
    @router.get("/repository/{business_id}", response_model=RepositoryClass.GetBusinessRequestModel, tags=["Repository"],
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.Repository.GetBusinessResponse}}}}
    )
    async def get_business_repository(
        business_id: str,
        repository: RepositoryClass.GetBusinessRequestModel = Body(..., example=Examples.Repository.GetBusinessRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Repository.Business.find_one(business_id) 
    
    
    
    @router.delete("/repository/{business_id}", response_model=TokensClass.DeleteResponseModel, tags=["Repository"],
        description="**Important**: Every folder and files inside will be delete", 
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.Repository.DeleteBusinessResponse}}}}
    )
    async def delete_business_repository(
        business_id: str,
        repository: RepositoryClass.DeleteBusinessRequestModel = Body(..., example=Examples.Repository.DeleteBusinessRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Repository.Business.delete(business_id) 
        
        
        
    @router.post("/repository/{user_id}", response_model=RepositoryClass.CreateUserRequestModel, tags=["Repository"],
        description="**Important**: The repository must be assigned to a business. This repository is automatically created with the business log, but can be deleted (cleaned) and recreated.", 
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.Repository.CreateUserResponse}}}}
    )
    async def create_user_repository(
        user_id: str,
        repository: RepositoryClass.CreateUserRequestModel = Body(..., example=Examples.Repository.CreateUserRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Repository.User.create(user_id) 
    
    
    
    @router.get("/repository/{user_id}", response_model=RepositoryClass.GetUserRequestModel, tags=["Repository"],
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.Repository.GetUserResponse}}}}
    )
    async def get_user_repository(
        user_id: str,
        repository: RepositoryClass.GetUserRequestModel = Body(..., example=Examples.Repository.GetUserRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Repository.User.find_one(user_id) 
    
    
    
    @router.delete("/repository/{user_id}", response_model=TokensClass.DeleteResponseModel, tags=["Repository"],
        description="**Important**: Every folder and files inside will be delete", 
        responses={200: {"description": "Successful Response", "content": {"application/json": {"example": Examples.Repository.DeleteUserResponse}}}}
    )
    async def delete_user_repository(
        user_id: str,
        repository: RepositoryClass.DeleteUserRequestModel = Body(..., example=Examples.Repository.DeleteUserRequest),
        current_user: APIClass.FindAPIUser = Depends(get_current_active_user)
    ):
        return Functions.Repository.User.delete(user_id) 
    
    ## FALTA AÑADIR MÁS RUTAS CÓMO CREAR Y ELIMINAR CARPETA, SUBIR Y ELIMINAR ARCHIVO, ACTUALIZAR REPOSITORIO
