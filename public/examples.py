from bson import ObjectId

class Examples:
    
    class Business:
            
        Create = {
            "profile": {
                "description": "Demo de Camping",
                "networks": {
                    "website": "https://softcamp.eu"
                }
            },
            "business": {
                "name": "SoftCamp",
                "legal_name": "SoftCamp Europe, S.L",
                "identity_number": "B90280595",
                "type": "company",
                "area": "camping",
                "spots": "1-80",
                "descriptor": "SoftCamp EMEA",
                "location": {
                    "address": "Calle bartolome de medina, 1",
                    "address2": None,
                    "city": "Sevilla",
                    "province": "Sevilla",
                    "country": "ES",
                    "zipcode": "41004",
                    "commercial": {
                        "address": "Calle bartolome de medina, 1",
                        "city": "Sevilla",
                        "country": "ES",
                        "province": "Sevilla",
                        "zipcode": "41004"
                    },
                },
                "contact": {
                    "email": "admin@globodain.com",
                    "phone": {
                        "prefix": "+34",
                        "number": "666444555"
                    }
                },
            },
            "stripe": {
                "mmc": "7033",
            },
            "subscription": {
                "plan": "platinum",
                "time": "free"
            },
            "camping": [],
            "settings": [],
            "onboarding": False,
            "installed_modules": []
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "659c3384adeeb8ef35fe1692"
        }
    
    class Invitations:
        Create = {
            'email': "ruben@globodain.com"
        }
        
        Get = {
            
        }
        
        Delete = {
            'email': "ruben@globodain.com"
        }
        
    class Users:
        
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class Roles:
        
        Create = {
            "type": "Recepcionist",
            "permissions": {
                "write": [
                    "booking_management",
                    "payment_management",
                    "oneway_management"
                ],
                "read": [
                    "booking_management",
                    "payment_management",
                    "oneway_management"
                ],
                "delete": [],
                "rewrite": []
            }
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class Bookings:
        
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class Customers:
        
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class Transactions:
        
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class Invoices:
        
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class Payments:
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class Prices:
        
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
    
    class Discounts:
        
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class Banks:
        
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class Services:
    
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
    
    class Persons:
        
        Create = {
            
        }
        
        Get = {
            
        }
        
        Delete = {
            '_id': "656741400e481ff94ded1f3f",
            'business_id': "656741400e481ff94ded1f3c"
        }
        
    class TasksLog:
        
        CreateRequest = {
            "business_id": "66754ebe20560978385df419"
        }
        
        CreateResponse = {
            "message": "Tasks Log was created successfully!"
        }
        
        GetRequest = {
            "business_id": "66754ebe20560978385df419"
        }
        
        GetResponse = {
            "business_id": {
                "$oid": "66754ebe20560978385df419"
            },
            "tasks": [
                {
                "title": "new_business",
                "msg": "Se ha creado el negocio con éxito",
                "code": 200,
                "status": "pending"
                },
                {
                "user_id": {
                    "$oid": "66754ec220560978385df41f"
                },
                "user_name": "Portilla",
                "title": "new_user",
                "msg": "Se ha creado un nuevo usuario: Portilla",
                "code": 200,
                "status": "pending",
                "created": {
                    "$date": "2024-06-21T11:58:28.363Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-21T12:10:28.064Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-21T12:10:41.787Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-21T12:11:46.870Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-21T12:12:28.516Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-21T12:13:00.340Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-24T09:11:52.601Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-24T09:14:01.968Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-24T09:14:55.246Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-24T09:16:31.761Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-24T09:17:00.242Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-24T09:18:39.490Z"
                }
                },
                {
                "user_id": "B90280595",
                "user_name": "Camping Puebla",
                "title": "already_business_exist",
                "msg": "Un usuario externo intentó registrar el mismo CIF/NIF",
                "code": 406,
                "status": "pending",
                "created": {
                    "$date": "2024-06-24T09:19:00.298Z"
                }
                }
            ],
            "created": {
                "$date": "2024-06-21T11:58:23.622Z"
            }
        }
        
        PushTaskRequest = {
            "title": "new_business",
            "msg": "The business has been successfully created!",
            "code": 200,
            "status": "pending"
        }
        
        PushTaskResponse = {
            "message": "The task was created successfully!"
        }
        
        DeleteRequest = {
            'business_id': "656741400e481ff94ded1f3c"
        }
        
        DeleteResponse = {
            "message": "Tasks Log was deleted successfully!"
        }
        
    class Repository:
        
        CreateBusinessRequest = {
            "business_id": "6639f41fe4ff635b497a2a53"
        }
        
        CreateBusinessResponse = {
            "_id": {
                "$oid": "6554ac4f981ec9e923bf08f5"
            },
            "business_id": {
                "$oid": "6639f41fe4ff635b497a2a53"
            },
            "status": "active",
            "created": {
                "$date": "2024-05-07T11:27:59.748Z"
            }
        }
        
        CreateUserRequest = {
            "user_id": "653a8eefcdc7b64e2c919cd3"
        }
        
        CreateUserResponse = {
            "_id": {
                "$oid": "653a8eefcdc7b64e2c919cd4"
            },
            "user_id": {
                "$oid": "653a8eefcdc7b64e2c919cd3"
            },
            "status": "active",
            "created": {
                "$date": "2024-05-07T11:27:59.748Z"
            }
        }
        
        GetBusinessRequest = {
            "business_id": "659c3383adeeb8ef35fe168f",
        }
        
        GetBusinessResponse = {
            "business_id": "659c3383adeeb8ef35fe168f",
            "status": "active",
            "folders": [{
                "title": "Bungalow images",
                "description": "Images from bungalow service",
                "color": "#FAFAFA",
                "files": [
                    {
                        "id": "aska28s2xlai22m?2",
                        "filename": "front-bungalow-22-office.jpg",
                        "uploaded": "2024-01-08T20:41:22.462+00:00"
                    }, {
                        "id": "el3mdi3k2s8k2ks?3",
                        "filename": "front-bungalow-23-office.jpg",
                        "uploaded": "2024-01-08T20:42:14.245+00:00"
                    }
                ],
                "status": "disabled"
            }],
        }
        
        GetUserRequest = {
            "user_id": "659c3384adeeb8ef35fe1691",
        }
        
        GetUserResponse = {
            "user_id": "659c3384adeeb8ef35fe1691",
            "status": "active",
            "folders": [{
                "title": "Bungalow images",
                "description": "Images from bungalow service",
                "color": "#FAFAFA",
                "files": [
                    {
                        "id": "aska28s2xlai22m?2",
                        "filename": "front-bungalow-22-office.jpg",
                        "uploaded": "2024-01-08T20:41:22.462+00:00"
                    }, {
                        "id": "el3mdi3k2s8k2ks?3",
                        "filename": "front-bungalow-23-office.jpg",
                        "uploaded": "2024-01-08T20:42:14.245+00:00"
                    }
                ],
                "status": "disabled"
            }],
        }
        
        DeleteBusinessRequest = {
            'business_id': "656741400e481ff94ded1f3c"
        }
        
        DeleteBusinessResponse = {
            "message": "Repository was deleted!"
        }
        
        DeleteUserRequest = {
            'user_id': "656741400e481ff94ded1f3c"
        }
        
        DeleteUserResponse = {
            "message": "Repository was deleted!"
        }
        
    class Tokens:
        
        CreateRequest = {
            "user_id": "653a8eefcdc7b64e2c919cd3",
        }
        
        CreateResponse = {
            'message': F'Access Token was created with Token ID ce63eef6-2fb4-11ef-9d5a-af0c72b965d2'
        }
        
        GetRequest = {
            "user_id": "653a8eefcdc7b64e2c919cd3",
        }
        
        GetResponse = {
            "_token": "de9cacc4-7419-11ee-8e87-00155db906bd",
            "user_id": "653a8eefcdc7b64e2c919cd3",
            "_last": "2024-02-09T09:08:03.318+00:00",
            "created": "2023-10-26T18:08:15.287+00:00"
        }
        
        DeleteRequest = {
            "user_id": "653a8eefcdc7b64e2c919cd3",
        }
        
        DeleteResponse = {
            "message": "Access Token was deleted successfully!"
        }

    
