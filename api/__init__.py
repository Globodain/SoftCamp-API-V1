#######################
#
#   A P I   F U N C T I O N S  
#
#######################

from api._banks import Banks
from api._bookings import Bookings
from api._business import Business
from api._customers import Customers
from api._discounts import Discounts
from api._invitations import Invitations
from api._invoices import Invoices
from api._payments import Payments
from api._persons import Persons
from api._prices import Prices
from api._roles import Roles
from api._repository import Repository
from api._services import Services
from api._transactions import Transactions
from api._tasks_log import Tasks_log
from api._tokens import Tokens
from api._users import Users

class Functions:
    Banks = Banks
    Bookings = Bookings
    Business = Business
    Customers = Customers
    Discounts = Discounts
    Invitations = Invitations
    Invoices = Invoices
    Payments = Payments
    Persons = Persons
    Prices = Prices
    Roles = Roles
    Repository = Repository
    Services = Services
    Transactions = Transactions
    Tasks_log = Tasks_log
    Tokens = Tokens
    Users = Users