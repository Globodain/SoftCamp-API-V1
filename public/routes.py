from fastapi import APIRouter, Request, Depends, HTTPException, Form, status, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId,json_util
from models._classes import CreateBusiness,GetBusinessModel,UpdateBusinessModel,APIToken,SuperAdmin,CreateAPIUser,FindAPIUser
from auth._control import oauth2_scheme,authenticate_user,get_password_hash,get_current_active_user,get_current_user,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,SUPERADMIN_PASSWORD,get_support_team
from config.db.connection import db_app,db_api
from datetime import timedelta
import json

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
        
    @router.get("/my-account", tags=['API User'], response_model=FindAPIUser)
    async def my_account(current_user: FindAPIUser = Depends(get_current_active_user)):
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
    async def login_for_access_token(response: Response, username: str = Form(...), password: str = Form(...)):
        user = authenticate_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user['username']}, expires_delta=access_token_expires
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
    
    @router.post("/token", include_in_schema=False, response_model=APIToken)
    def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user['username']}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

class Admin:
        
    @router.post("/add_user", include_in_schema=False)
    async def add_user(user: CreateAPIUser, admin: SuperAdmin):
        # Check if the provided password is correct
        if admin.password != SUPERADMIN_PASSWORD:
            raise HTTPException(status_code=400, detail="Incorrect superadmin password")

        # Check if the username already exists in the database
        if db_api.users.find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail="Username already exists")

        # Hash the user's password
        hashed_password = get_password_hash(user.password)

        # Insert the new user into the database
        db_api.users.insert_one({
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "hashed_password": hashed_password,
            "disabled": user.disabled,
            "softcamp_team": user.softcamp_team
        })

        return {"message": "User added successfully"}

class ApiUsers:

    @router.get("/users", tags=["API User"], include_in_schema=False)
    async def get_users(current_user: dict = Depends(get_support_team)):
        # Query the database for all users
        user_list = list(db_api.users.find())

        # Convert ObjectId's to strings
        for user in user_list:
            user["_id"] = str(user["_id"])

        return user_list

class Business:

    business_objects = {}

    @router.post("/business", tags=["Business"], include_in_schema=False)
    async def create_business(item: CreateBusiness, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": item}
    
    @router.get("/business/{business_id}", response_model=GetBusinessModel, tags=["Business"])
    async def get_business(business_id: str,
                           user: FindAPIUser = Depends(get_current_active_user)):
        
        query = db_app.business.find_one({'_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this business id. Check it and try again"}
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    @router.put("/business/{business_id}", response_model=UpdateBusinessModel, tags=["Business"])
    async def update_business(business_id: str, business: UpdateBusinessModel, user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.business.update_one({'_id': ObjectId(business_id)}, {"$set": business()})
        if query is None:
            return {"message": "We can't find this business id. Check it and try again"}
        updated_business = db_app.business.find_one({'_id': ObjectId(business_id)})
        return updated_business

class Users:
    from models._classes import InviteUser,CreateUser,GetUsers,GetUser,UpdateUser,DeleteUser
    users_objects = {}

    @router.post("/invite/{business_id}", tags=["Users"])
    async def invite_user(business_id: str, user: InviteUser, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": user}

    @router.post("/users/{business_id}", tags=["Users"])
    async def create_user(business_id: str, user: CreateUser, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": user}
    
    @router.get("/users/{business_id}", response_model=GetUsers, tags=["Users"])
    async def get_users(business_id: str,
                           current_user: FindAPIUser = Depends(get_current_active_user)):
        
        query = db_app.users.find({'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this business id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)
    
    @router.get("/users/{business_id}/{user_id}", response_model=GetUser, tags=["Users"])
    async def get_user(business_id: str,
                           user_id: str,
                           current_user: FindAPIUser = Depends(get_current_active_user)):
        
        query = db_app.users.find_one({'_id': ObjectId(user_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this user id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    @router.put("/users/{business_id}/{user_id}", response_model=UpdateUser, tags=["Users"])
    async def update_user(business_id: str, user_id: str, user: UpdateUser, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.users.update_one({'_id': ObjectId(user_id), 'business_id': ObjectId(business_id)}, {"$set": user()})
        if query is None:
            return {"message": "We can't find this user id. Check it and try again"}
        update_user = db_app.users.find_one({'_id': ObjectId(user_id), 'business_id': ObjectId(business_id)})
        return update_user
    
    @router.delete("/users/{business_id}/{user_id}", response_model=UpdateUser, tags=["Users"])
    async def delete_user(business_id: str, user_id: str, user: UpdateUser, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.users.delete_one({'_id': ObjectId(user_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this user id. Check it and try again"}
        return {"message": "User was deleted successfully!"}

class Roles:
    from models._classes import CreateRole,GetRoles,GetRole,UpdateRole,DeleteRole
    roles_objects = {}
    
    @router.post("/roles/{business_id}", response_model=CreateRole, tags=["Roles"])
    async def create_role(business_id: str, role: CreateRole, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": role}
    
    @router.get("/roles/{business_id}", response_model=GetRoles, tags=["Roles"])
    async def get_role(business_id: str, roles: GetRoles, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.roles.find({'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this business id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)
    
    @router.get("/roles/{business_id}/{role_id}", response_model=GetRole, tags=["Roles"])
    async def get_role(business_id: str, role_id: str, role: GetRole, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.roles.find_one({'_id': ObjectId(role_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this role id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    @router.put("/roles/{business_id}/{role_id}", response_model=UpdateRole, tags=["Roles"])
    async def update_role(business_id: str, role_id: str, role: UpdateRole, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.roles.update_one({'_id': ObjectId(role_id), 'business_id': ObjectId(business_id)}, {"$set": role()})
        if query is None:
            return {"message": "We can't find this role id. Check it and try again"}
        update_role = db_app.roles.find_one({'_id': ObjectId(role_id), 'business_id': ObjectId(business_id)})
        return update_role

    @router.delete("/roles/{business_id}/{role_id}", response_model=DeleteRole, tags=["Roles"])
    async def delete_user(business_id: str, role_id: str, role: DeleteRole, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.roles.delete_one({'_id': ObjectId(role_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this role id. Check it and try again"}
        return {"message": "Role was deleted successfully!"}

class Bookings:
    from models._classes import CreateBooking,GetBookings,GetBooking,UpdateBooking,AddAccommodation,DeleteBooking
    booking_objects = {}
    
    @router.post("/bookings/{business_id}", response_model=CreateBooking, tags=["Bookings"])
    async def create_booking(business_id: str, booking: CreateBooking, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": booking}
    
    @router.get("/bookings/{business_id}", response_model=GetBookings, tags=["Bookings"])
    async def get_booking(business_id: str, bookings: GetBookings, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.bookings.find({'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this business id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)
    
    @router.get("/bookings/{business_id}/{booking_id}", response_model=GetBooking, tags=["Bookings"])
    async def get_booking(business_id: str, booking_id: str, booking: GetBooking, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.bookings.find_one({'_id': ObjectId(booking_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this booking id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    @router.put("/bookings/{business_id}/{booking_id}", response_model=UpdateBooking, tags=["Bookings"])
    async def update_booking(business_id: str, booking_id: str, booking: UpdateBooking, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.bookings.update_one({'_id': ObjectId(booking_id), 'business_id': ObjectId(business_id)}, {"$set": booking()})
        if query is None:
            return {"message": "We can't find this booking id. Check it and try again"}
        update_booking = db_app.bookings.find_one({'_id': ObjectId(booking_id), 'business_id': ObjectId(business_id)})
        return update_booking

    @router.put("/bookings/{business_id}/{booking_id}/{spot_id}", response_model=AddAccommodation, tags=["Bookings"])
    async def add_other_accomodation_to_booking(business_id: str, booking_id: str, spot_id: str, booking: AddAccommodation, current_user: FindAPIUser = Depends(get_current_active_user)):
        ## Revisar cómo se asigna el spot
        query = db_app.bookings.update_one({'_id': ObjectId(booking_id), 'business_id': ObjectId(business_id)}, {"$set": booking()})
        if query is None:
            return {"message": "We can't find this booking or spot id. Check it and try again"}
        update_booking = db_app.bookings.find_one({'_id': ObjectId(booking_id), 'business_id': ObjectId(business_id)})
        return update_booking

    @router.delete("/bookings/{business_id}/{booking_id}", response_model=DeleteBooking, tags=["Bookings"])
    async def delete_booking(business_id: str, booking_id: str, booking: DeleteBooking, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.bookings.delete_one({'_id': ObjectId(booking_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this booking id. Check it and try again"}
        return {"message": "Booking was deleted successfully!"}

    
class Customers:
    from models._classes import CreateCustomer,GetCustomers,GetCustomer,UpdateCustomer,DeleteCustomer
    customer_objects = {}
    
    @router.post("/customers/{business_id}", response_model=CreateCustomer, tags=["Customers"])
    async def create_customer(business_id: str, customer: CreateCustomer, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": customer}
    
    @router.get("/customers/{business_id}", response_model=GetCustomers, tags=["Customers"])
    async def get_customers(business_id: str, customers: GetCustomers, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.customers.find({'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this customer id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)
    
    @router.get("/customers/{business_id}/{customer_id}", response_model=GetCustomer, tags=["Customers"])
    async def get_customer(business_id: str, customer_id: str, customer: GetCustomer, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.customers.find_one({'_id': ObjectId(customer_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this role id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    @router.put("/customers/{business_id}/{customer_id}", response_model=UpdateCustomer, tags=["Customers"])
    async def update_customer(business_id: str, customer_id: str, customer: UpdateCustomer, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.customers.update_one({'_id': ObjectId(customer_id), 'business_id': ObjectId(business_id)}, {"$set": customer()})
        if query is None:
            return {"message": "We can't find this booking id. Check it and try again"}
        update_customer = db_app.customers.find_one({'_id': ObjectId(customer_id), 'business_id': ObjectId(business_id)})
        return update_customer

    @router.delete("/customers/{business_id}/{customer_id}", response_model=DeleteCustomer, tags=["Customers"])
    async def delete_customer(business_id: str, customer_id: str, customer: DeleteCustomer, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.customers.delete_one({'_id': ObjectId(customer_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this customer id. Check it and try again"}
        return {"message": "Customer was deleted successfully!"}
    
class Transactions:
    from models._classes import CreateTransaction,GetTransactions,GetTransaction,UpdateTransaction,DeleteTransaction
    transactions_objects = {}
    
    @router.post("/transactions/{business_id}", response_model=CreateTransaction, tags=["Transactions"])
    async def create_transaction(business_id: str, transaction: CreateTransaction, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": transaction}
    
    @router.get("/transactions/{business_id}", response_model=GetTransactions, tags=["Transactions"])
    async def get_transactions(business_id: str, transaction: GetTransactions, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.transactions.find({'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this business id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)
    
    @router.get("/transactions/{business_id}/{transaction_id}", response_model=GetTransaction, tags=["Transactions"])
    async def get_transaction(business_id: str, transaction_id: str, transaction: GetTransaction, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.transactions.find_one({'_id': ObjectId(transaction_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this transaction id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    @router.put("/transactions/{business_id}/{transaction_id}", response_model=UpdateTransaction, tags=["Transactions"])
    async def update_transaction(business_id: str, transaction_id: str, transaction: UpdateTransaction, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.transactions.update_one({'_id': ObjectId(transaction_id), 'business_id': ObjectId(business_id)}, {"$set": transaction()})
        if query is None:
            return {"message": "We can't find this transaction id. Check it and try again"}
        update_transaction = db_app.transactions.find_one({'_id': ObjectId(transaction_id), 'business_id': ObjectId(business_id)})
        return update_transaction

    @router.delete("/transactions/{business_id}/{transaction_id}", response_model=DeleteTransaction, tags=["Transactions"])
    async def delete_transaction(business_id: str, transaction_id: str, transaction: DeleteTransaction, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.transactions.delete_one({'_id': ObjectId(transaction_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this transaction id. Check it and try again"}
        return {"message": "Transaction was deleted successfully!"}

 
class Invoices:
    from models._classes import CreateInvoice,GetInvoices,GetInvoice,UpdateInvoice,DeleteInvoice
    invoices_objects = {}
    
    @router.post("/invoices/{business_id}", response_model=CreateInvoice, tags=["Invoices"])
    async def create_invoice(business_id: str, invoice: CreateInvoice, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": invoice}
    
    @router.get("/invoices/{business_id}", response_model=GetInvoices, tags=["Invoices"])
    async def get_invoices(business_id: str, invoices: GetInvoices, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.invoices.find({'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this business id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)
    
    @router.get("/invoices/{business_id}/{invoice_id}", response_model=GetInvoice, tags=["Invoices"])
    async def get_transaction(business_id: str, invoice_id: str, invoice: GetInvoice, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.invoices.find_one({'_id': ObjectId(invoice_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this invoice id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    @router.put("/invoices/{business_id}/{invoice_id}", response_model=UpdateInvoice, tags=["Invoices"])
    async def update_invoice(business_id: str, invoice_id: str, invoice: UpdateInvoice, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.invoices.update_one({'_id': ObjectId(invoice_id), 'business_id': ObjectId(business_id)}, {"$set": invoice()})
        if query is None:
            return {"message": "We can't find this invoice id. Check it and try again"}
        update_invoices = db_app.invoices.find_one({'_id': ObjectId(invoice_id), 'business_id': ObjectId(business_id)})
        return update_invoices

    @router.delete("/invoices/{business_id}/{invoice_id}", response_model=DeleteInvoice, tags=["Invoices"])
    async def delete_invoice(business_id: str, invoice_id: str, invoice: DeleteInvoice, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.invoices.delete_one({'_id': ObjectId(invoice_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this invoice id. Check it and try again"}
        return {"message": "Invoice was deleted successfully!"}


class Payments:
    from models._classes import CreatePayment,GetPayments,GetPayment,UpdatePayment,DeletePayment
    payments_objects = {}
    
    @router.post("/payments/{business_id}", response_model=CreatePayment, tags=["Payments"])
    async def create_payment(business_id: str, payment: CreatePayment, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": payment}
    
    @router.get("/payments/{business_id}", response_model=GetPayments, tags=["Payments"])
    async def get_payments(business_id: str, payments: GetPayments, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.payments.find({'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this business id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)
    
    @router.get("/payments/{business_id}/{payment_id}", response_model=GetPayment, tags=["Payments"])
    async def get_payment(business_id: str, payment_id: str, payment: GetPayment, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.payments.find_one({'_id': ObjectId(payment_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this payment id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    @router.put("/payments/{business_id}/{payment_id}", response_model=UpdatePayment, tags=["Payments"])
    async def update_payment(business_id: str, payment_id: str, payment: UpdatePayment, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.payments.update_one({'_id': ObjectId(payment_id), 'business_id': ObjectId(business_id)}, {"$set": payment()})
        if query is None:
            return {"message": "We can't find this payment id. Check it and try again"}
        update_payment = db_app.payments.find_one({'_id': ObjectId(payment_id), 'business_id': ObjectId(business_id)})
        return update_payment

    @router.delete("/payments/{business_id}/{payment_id}", response_model=DeletePayment, tags=["Payments"])
    async def delete_payment(business_id: str, payment_id: str, payment: DeletePayment, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.payments.delete_one({'_id': ObjectId(payment_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this payment id. Check it and try again"}
        return {"message": "Invoice was deleted successfully!"}


class Prices:
    from models._classes import CreatePrice,GetPrices,GetPrice,UpdatePrice,DeletePrice
    prices_object = {}
    
    @router.post("/prices/{business_id}", response_model=CreatePrice, tags=["Prices"])
    async def create_price(business_id: str, price: CreatePrice, 
                              current_user: dict = Depends(get_current_user)):
        return {"item": price}
    
    @router.get("/prices/{business_id}", response_model=GetPrices, tags=["Prices"])
    async def get_prices(business_id: str, prices: GetPrices, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.prices.find({'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this business id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)
    
    @router.get("/prices/{business_id}/{price_id}", response_model=GetPrice, tags=["Prices"])
    async def get_payment(business_id: str, price_id: str, price: GetPrice, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.prices.find_one({'_id': ObjectId(price_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this price id. Check it and try again"}
        
        json_str = json_util.dumps(query)
        data = json.loads(json_str)
        return JSONResponse(content=data)

    @router.put("/prices/{business_id}/{price_id}", response_model=UpdatePrice, tags=["Prices"])
    async def update_price(business_id: str, price_id: str, price: UpdatePrice, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.prices.update_one({'_id': ObjectId(price_id), 'business_id': ObjectId(business_id)}, {"$set": price()})
        if query is None:
            return {"message": "We can't find this payment id. Check it and try again"}
        update_price = db_app.prices.find_one({'_id': ObjectId(price_id), 'business_id': ObjectId(business_id)})
        return update_price

    @router.delete("/prices/{business_id}/{price_id}", response_model=DeletePrice, tags=["Prices"])
    async def delete_payment(business_id: str, price_id: str, price: DeletePrice, current_user: FindAPIUser = Depends(get_current_active_user)):
        query = db_app.prices.delete_one({'_id': ObjectId(price_id), 'business_id': ObjectId(business_id)})
        if query is None:
            return {"message": "We can't find this price id. Check it and try again"}
        return {"message": "Invoice was deleted successfully!"}

