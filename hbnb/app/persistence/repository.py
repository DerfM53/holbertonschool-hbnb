from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        if obj is None:
            raise ValueError("Cannot add None object to repository")
        if not hasattr(obj, 'id') or obj.id is None:
            raise ValueError("Object must have an 'id' attribute")
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        obj = self._storage.get(obj_id)
        if obj is None:
            print(f"Object with ID {obj_id} not found in repository")  # Log pour le débogage
        return obj

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
        return obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)
    
    def find_by_email(self, email):
        return next((user for user in self._storage.values() if getattr(user, 'email', None) == email), None)
    