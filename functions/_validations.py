from bson import ObjectId

class Validations:
        
    def is_valid_object_id(str_id):
        return ObjectId.is_valid(str_id)