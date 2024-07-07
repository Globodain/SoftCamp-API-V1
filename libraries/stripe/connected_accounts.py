from fastapi import HTTPException, status
import stripe

class ConnectedAccounts:
    
    def delete_one(account_id: str, reason: str):
        try:
            stripe.Account.delete(account_id, reason=reason)
            return {'message': "Connected Account was deleted sucessfull!"}
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="We can't find this Connected Account ID",
                headers={"WWW-Authenticate": "Bearer"},
            )