from nest.core import Module
from src.providers.potiguar_lookup.potiguar_lookup_module import PotiguarLookupModule
from .tasks_service import TasksService

@Module(
    imports=[PotiguarLookupModule],
    providers=[TasksService],
)   
class TasksModule:
    pass

    