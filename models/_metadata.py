import os
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

tags_metadata = [
    {
        "name": "API User",
        "description": "",
        "externalDocs": {
            "description": "How works the authentication",
            "url": f"{BASE_URL}/documentation/authentication",
        },
    },
    {
        "name": "Business",
        "description": "",
        "externalDocs": {
            "description": "What is a 'Business' and how works",
            "url": f"{BASE_URL}/documentation/business",
        },
    },
    {
        "name": "Invitations",
        "description": "",
    },
    {
        "name": "Users",
        "description": "",
    },
    {
        "name": "Roles",
        "description": "",
    },
    {
        "name": "Bookings",
        "description": "",
    },
    {
        "name": "Customers",
        "description": "",
    },
    {
        "name": "Transactions",
        "description": "",
    },
    {
        "name": "Invoices",
        "description": "",
    },
    {
        "name": "Payments",
        "description": "",
    },
    {
        "name": "Prices",
        "description": "",
    },
    {
        "name": "Discounts",
        "description": "",
    },
    {
        "name": "Banks",
        "description": "",
    },
    {
        "name": "Services",
        "description": "",
    },
    {
        "name": "Persons",
        "description": "",
    },
    {
        "name": "TasksLog",
        "description": "",
    },
    {
        "name": "Repository",
        "description": "",
    },
]