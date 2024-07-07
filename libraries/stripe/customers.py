from fastapi import HTTPException, status
import stripe

class Customers:
    
    def delete_one(customer_id: str):
        try:
            stripe.Customer.delete(customer_id)
            return {'message': "Customer was deleted sucessfull!"}
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="We can't find this Customer ID",
                headers={"WWW-Authenticate": "Bearer"},
            )