import datetime

class Resource:
    r_id = 1
    def __init__(self, type_name: str, status: str = 'available'):
        self.id = "R-" + str(Resource.r_id)
        Resource.r_id +=1
        self.type = type_name
        self.status = status

    def __repr__(self) -> str:
        return f"Resource(id={self.id}, type='{self.type}', status='{self.status}')"
    

    

class AuditMixin:
    def log_action(self, action: str) -> None:
        timestamp = datetime.datetime.now()
        obj_id = getattr(self, 'id', 'System')
        print(f"[{timestamp}] [ID:{str(obj_id)[:6]}] {action}")

class ResourceCatalog(AuditMixin):

    def __init__(self):
        self._inventory= []

    def add_resource(self, resource: Resource) -> None:
        self._inventory.append(resource)

    def __len__(self) -> int:
        return len(self._inventory)

    def __iter__(self):
        return iter(self._inventory)

    def allocate(self, requester):
        if not hasattr(requester, 'needs_resource') or not hasattr(requester, 'id'):
            self.log_action(f"{requester} is not a valid requester.")
            return None

        if requester.needs_resource():
            for res in self._inventory:
                if res.status == 'available':
                    res.status = 'reserved' 
                    print(f"Catalog: Allocated {res.type} to ID {requester.id}")
                    return res
            self.log_action("Catalog: No available resources.")
            return None
        else:
            self.log_action(f"Catalog: Requester {requester.name} does not need resources.")
            return None
        

