from nest.core import Injectable
from src.providers.potiguar_lookup.potiguar_lookup_service import PotiguarLookupService

@Injectable
class TasksService:

    def __init__(self, potiguar_lookup_service: PotiguarLookupService):
        self.potiguar_lookup_service = potiguar_lookup_service


    async def add_tasks(self):
        pass
    
    async def get_tasks(self):
        pass
