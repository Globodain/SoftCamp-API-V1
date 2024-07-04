from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class Components:
    
    class Phone(BaseModel):
        prefix: str
        number: str

    class MapSettings(BaseModel):
        width: str
        height: str
        href: str
        x: str
        y: str

class General:

    class Contact(BaseModel):
        email: str
        phone: Components.Phone

    class Location(BaseModel):
        address: str
        address2: Optional[str] = None
        city: str
        province: str
        country: str
        zip: str

    class BaseMap(BaseModel):
        file: str
        mapExtension: str
        viewBox: str
        mapSettings: Components.MapSettings
        properties: dict

    class Capacity(BaseModel):
        people: int
        vehicles: int
    
    class Networks(BaseModel):
        website: str
        instagram: str
        facebook: str

class BusinessSubclass:

    class Profile(BaseModel):
        username: str
        description: str
        avatar: str
        logotipo: str
        networks: General.Networks
        verified: bool
        
    class Information(BaseModel):
        name: str
        legal_name: str
        identity_number: str
        type: str
        area: str
        spots: str
        descriptor: str
        location: General.Location
        contact: General.Contact
        marketplace: bool
        verified: bool

    class Subscription(BaseModel):
        subscription_id: str
        plan: str
        time: str
        next_renewal: datetime
        
    class Camping(BaseModel):
        seasons: dict
        services: List[str]
        capacity: General.Capacity
        control: dict
        baseMap: General.BaseMap
        
    class Stripe(BaseModel):
        account: str
        customer_id: str
        type: str
        mmc: str # Referrer to company activity code
        verified: bool
    
    class Martina(BaseModel):
        tokens: str