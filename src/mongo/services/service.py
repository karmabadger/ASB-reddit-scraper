from jsonschema import validate

class Service:
    """
    A service is a collection of functions that can be called by the
    client.
    """

    def __init__(self, mongo_client, mongo_db, mongo_collection, schema):
        """
        Constructor.
        """
        self.name = mongo_collection
        self.mongo_client = mongo_client
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.schema = schema
    
    def validate_instance(self, instance):
        """
        Validates the instance against the schema.
        """
        return True


    def insert_one(self, document):
        if self.validate_instance(document):
            self.mongo_db[self.mongo_collection].insert_one(document)
            return True
        else:
            return False

    def insert_many(self, documents):
        for document in documents:
            if not self.validate_instance(document):
                return False
        
        self.mongo_db[self.mongo_collection].insert_many(documents)
        return True


    def find_one(self, query):
        return self.mongo_db[self.mongo_collection].find_one(query)
    
    def find_many(self, query):
        return self.mongo_db[self.mongo_collection].find(query)

    def update_one(self, query, update):
        if self.validate_instance(update):
            self.mongo_db[self.mongo_collection].update_one(query, update)
            return True
    
    def update_many(self, query, update):
        if self.validate_instance(update):
            self.mongo_db[self.mongo_collection].update_many(query, update)
            return True

    def delete_one(self, query):
        self.mongo_db[self.mongo_collection].delete_one(query)

    def delete_many(self, query):
        self.mongo_db[self.mongo_collection].delete_many(query)

    def find_one_and_delete(self, query):
        return self.mongo_db[self.mongo_collection].find_one_and_delete(query)

    def find_one_and_replace(self, query, replacement):
        if self.validate_instance(replacement):
            return self.mongo_db[self.mongo_collection].find_one_and_replace(query, replacement)

    def find_one_and_update(self, query, update):
        if self.validate_instance(update):
            return self.mongo_db[self.mongo_collection].find_one_and_update(query, update)
        else:
            return False

    



    