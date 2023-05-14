

class Controller:
    def __init__(self, service):
        self.service = service

    def insert_one(self, document):
        return self.service.insert_one(document)

    def insert_many(self, documents):
        return self.service.insert_many(documents)    

    
    def find_one_by_id(self, id):
        return self.service.find_one_by_id(id)

    def find_one_by_id_and_update(self, id, document):
        return self.service.find_one_and_update(id, document)

    def find_one_by_id_and_delete(self, id):
        return self.service.find_one_by_id_and_delete(id)

